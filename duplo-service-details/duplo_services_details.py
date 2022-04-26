import requests
import json
import os


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


def fetch_duplo_service_details(host, tenant, tenant_id, token, services_array):
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
        service_details = []
        include_all = ('all' in services_array)
        # Loop through response contents and fill out data for running services
        # If the Duplo service name contains 'duploinfrasvc', then ignore it when adding data to service_details
        for service in duplo_response:
            service_name = service["Name"]
            if (include_all and not service_name.endswith('duploinfrasvc')) or (service_name in services_array):
                ecr_repo, i, image_tag = service["Containers"][0]["Image"].rpartition('/')
                service_details.append(f"{image_tag}")
    return service_details


def run_action() -> None:
    # host, tenant, tenant_id, token, services
    host = os.environ["INPUT_HOST"]
    tenant = os.environ["INPUT_TENANT"]
    # tenant_id = os.environ["INPUT_TENANT_ID"]
    token = os.environ["INPUT_TOKEN"]
    services = os.environ["INPUT_SERVICES"]

    try:
        tenant_id = fetch_duplo_tenant_id(host, tenant, token)

        if services != '':
            services_array = json.loads(services)
        else:
            services_array = ['all']
        service_details = fetch_duplo_service_details(host, tenant, tenant_id, token, services_array)
        print(f"::set-output name=service_details::{json.dumps(service_details)}{os.linesep}")
    except Exception as e:
        print(f"::error ::{str(e)}{os.linesep}")
        raise e


if __name__ == "__main__":
    run_action()
