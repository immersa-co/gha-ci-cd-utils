import requests
import json
import os
import time

# TODO: Future enhancement create an action to look up all tenants and Ids using
#   https://immersa-dev.duplocloud.net/admin/GetTenantsForUser
#   response is an array of maps with 2 keys of interest
#   [{..."TenantId":"<id>","AccountName":"<name>","...}, ...]


def fetch_duplo_services(host, tenant, tenant_id, token, services_array):
    # Send GET request to Duplo API to get service information
    duplo_url = f'{host}/subscriptions/{tenant_id}/GetPods'
    duplo_headers = {'Authorization': f"Bearer {token}"}

    response = requests.get(duplo_url, headers=duplo_headers)

    if not response.ok:
        print(f'Trouble Getting services for {tenant} from duplo cloud {duplo_url} ')
        print(response.content)
        raise Exception(response.json())
    else:
        # process and get the service list
        duplo_response = json.loads(response.content.decode())
        # Initializing dictionary to hold scraped data
        running_services = []
        failed_service_dict = dict()
        failed_service = False
        include_all = ('all' in services_array)
        # If the Duplo service name contains this string, then ignore it when adding data to services_dict
        # Loop through response contents and fill out data for running services
        for service in duplo_response:
            service_name = service["Name"]
            if (include_all and not service_name.endswith('duploinfrasvc')) or (service_name in services_array):
                status = service["CurrentStatus"]
                if status == 1:
                    running_services.append(service_name)
                else:
                    failed_service_dict[service_name] = status
    return running_services, failed_service_dict


def run_action() -> None:
    # host, tenant, tenant_id, token, services
    host = os.environ["INPUT_HOST"]
    tenant = os.environ["INPUT_TENANT"]
    tenant_id = os.environ["INPUT_TENANT_ID"]
    token = os.environ["INPUT_TOKEN"]
    services = os.environ["INPUT_SERVICES"]
    max_attempts_str = os.environ["INPUT_MAX_ATTEMPTS"]
    retry_delay = os.environ["INPUT_RETRY_DELAY"]

    try:
        if services != '':
            services_array = json.loads(services)
        else:
            services_array = ['all']
        running_services = []
        failed_service_dict = dict()
        max_attempts = int(max_attempts_str)
        while max_attempts > 0:
            running_services, failed_service_dict = fetch_duplo_services(host, tenant, tenant_id, token, services_array)
            if len(running_services) == len(services_array) and len(failed_service_dict) == 0:
                break
            else:
                max_attempts = max_attempts - 1
                if max_attempts > 0:
                    time.sleep(int(retry_delay))
        print(f"::set-output name=running_services::{running_services}{os.linesep}")
        print(f"::set-output name=failed_service_dict::{json.dumps(failed_service_dict)}{os.linesep}")
        print(f"::set-output name=result::{len(running_services) == len(services_array)}{os.linesep}")
    except Exception as e:
        print(f"::error ::{str(e)}{os.linesep}")
        raise e


if __name__ == "__main__":
    run_action()
