import requests
import json
import os
import time
import timeit

# TODO: Future enhancement create an action to look up all tenants and Ids using
#   https://immersa-dev.duplocloud.net/admin/GetTenantsForUser
#   response is an array of maps with 2 keys of interest
#   [{..."TenantId":"<id>","AccountName":"<name>","...}, ...]


def fetch_duplo_tenant_id(host, tenant, token):
    duplo_url = f'{host}/admin/GetTenantsForUser'
    duplo_headers = {'Authorization': f"Bearer {token}"}
    response = requests.get(duplo_url, headers=duplo_headers)
    if not response.ok:
        print(f'Trouble Getting tenantId for {tenant} from duplo cloud {duplo_url} ')
        print(response.content)
        raise Exception(response.json())
    else:
        arr = list(filter(lambda item: item['AccountName'] == tenant, json.loads(response.content.decode())))
        return arr[0]["TenantId"]


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
        only_pending_status = True
        for service in duplo_response:
            service_name = service["Name"]
            if (include_all and not service_name.endswith('duploinfrasvc') and not service_name == "prefect-agent") \
                    or (service_name in services_array):
                status = service["CurrentStatus"]
                ecr_repo, i, image_tag = service["Containers"][0]["Image"].rpartition('/')
                if status == 1:
                    running_services.append(f"{image_tag}")
                else:
                    # Ignore Deleted status for adding to failed services
                    if status != 6:
                        failed_service_dict[f"{image_tag}"] = status
                    if status != 3 and status != 6:
                        only_pending_status = False
    return running_services, failed_service_dict, only_pending_status


def run_action() -> None:
    start = timeit.timeit()

    # host, tenant, tenant_id, token, services
    host = os.environ["INPUT_HOST"]
    tenant = os.environ["INPUT_TENANT"]
    # tenant_id = os.environ["INPUT_TENANT_ID"]
    token = os.environ["INPUT_TOKEN"]
    services = os.environ["INPUT_SERVICES"]
    max_attempts_str = os.environ["INPUT_MAX_ATTEMPTS"]
    retry_delay = os.environ["INPUT_RETRY_DELAY"]

    try:
        tenant_id = fetch_duplo_tenant_id(host, tenant, token)

        if services != '':
            services_array = json.loads(services)
        else:
            services_array = ['all']
        running_services = []
        failed_service_dict = dict()
        max_attempts = int(max_attempts_str)
        while max_attempts > 0:
            running_services, failed_service_dict, only_pending_status = \
                fetch_duplo_services(host, tenant, tenant_id, token, services_array)
            if len(failed_service_dict) == 0:
                break
            else:
                print(f"Failed:[{json.dumps(failed_service_dict)}], Running: [{running_services}], "
                      f"Result: [{len(failed_service_dict) == 0}]")
                max_attempts = max_attempts - 1
                if max_attempts > 0 and only_pending_status:
                    time.sleep(int(retry_delay))
                else:
                    print(f"Giving up after {max_attempts_str} attempts, there are services not "
                          f"in running status. {json.dumps(failed_service_dict)}. remaining attempts {max_attempts}. "
                          f"only_pending_status is [{only_pending_status}], result is "
                          f"[{len(failed_service_dict) == 0 and len(running_services) > 0}]")
                    break
        end = timeit.timeit()
        print(f"::set-output name=time_elapsed::{end - start}{os.linesep}")
        print(f"::set-output name=running_services::{running_services}{os.linesep}")
        print(f"::set-output name=failed_service_dict::{json.dumps(failed_service_dict)}{os.linesep}")
        print(f"::set-output name=result::{len(failed_service_dict) == 0 and len(running_services) > 0}{os.linesep}")
    except Exception as e:
        print(f"::error ::{str(e)}{os.linesep}")
        raise e


def debug_python_directly():
    os.environ["INPUT_HOST"] = "https://immersa-dev.duplocloud.net/"
    os.environ["INPUT_TENANT"] = "dev01"
    os.environ["INPUT_TOKEN"] = os.getenv("DDT")
    os.environ["INPUT_SERVICES"] = '["postgres"]'
    os.environ["INPUT_MAX_ATTEMPTS"] = "5"
    os.environ["INPUT_RETRY_DELAY"] = "1"


if __name__ == "__main__":
    # debug_python_directly()
    run_action()
