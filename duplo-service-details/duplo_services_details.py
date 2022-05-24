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


def fetch_duplo_service_details(host, tenant, tenant_id, token, services_array, filter_image_tags):
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
        service_change_details = dict()
        service_change_details["change-request"] = dict()
        service_change_details["change-request"]["z-currently-running"] = dict()
        service_change_details["change-request"]["z-filtered-services"] = dict()
        include_all = ('all' in services_array)
        filter_tags = len(filter_image_tags) > 0
        # Loop through response contents and fill out data for running services
        # If the Duplo service name contains 'duploinfrasvc', then ignore it when adding data to service_details
        for service in duplo_response:
            service_name = service["Name"]
            if (include_all and not service_name.endswith('duploinfrasvc') and not service_name == "prefect-agent") \
                    or (service_name in services_array):
                ecr_repo, i, image_tag = service["Containers"][0]["Image"].rpartition('/')
                service_details.append(f"{image_tag}")
                ecr_repo, i, image_tag = service["Containers"][0]["Image"].rpartition(':')
                config_tag_sha, dash, run_id = image_tag.rpartition('-')
                if "-" in config_tag_sha:
                    config_tag, dash, sha = config_tag_sha.rpartition('-')
                elif config_tag_sha != '':
                    config_tag = config_tag_sha
                else:
                    config_tag = 'main'

                if filter_tags and not image_tag.startswith(tuple(filter_image_tags)):
                    service_change_details["change-request"]["z-filtered-services"][service_name] = dict()
                    service_change_details["change-request"]["z-filtered-services"][service_name][
                        "image-tag"] = image_tag
                    service_change_details["change-request"]["z-filtered-services"][service_name][
                        "config-ref"] = config_tag
                    service_change_details["change-request"]["z-filtered-services"][service_name][
                        "current-state"] = service["CurrentStatus"]
                else:
                    service_change_details["change-request"]["z-currently-running"][service_name] = dict()
                    service_change_details["change-request"]["z-currently-running"][service_name][
                        "image-tag"] = image_tag
                    service_change_details["change-request"]["z-currently-running"][service_name][
                        "config-ref"] = config_tag
                    service_change_details["change-request"]["z-currently-running"][service_name][
                        "current-state"] = service["CurrentStatus"]

    return service_details, service_change_details


def run_action() -> None:
    # host, tenant, tenant_id, token, services
    host = os.environ["INPUT_HOST"]
    tenant = os.environ["INPUT_TENANT"]
    # tenant_id = os.environ["INPUT_TENANT_ID"]
    token = os.environ["INPUT_TOKEN"]
    services = os.environ["INPUT_SERVICES"]
    filter_tags = os.environ["INPUT_FILTER_TAGS"]

    if filter_tags is None or filter_tags == '':
        filter_image_tags = []
    else:
        filter_image_tags = json.loads(filter_tags)

    try:
        tenant_id = fetch_duplo_tenant_id(host, tenant, token)

        if services != '':
            services_array = json.loads(services)
        else:
            services_array = ['all']
        service_details, service_change_details = fetch_duplo_service_details(host, tenant, tenant_id, token, \
                                                                              services_array, filter_image_tags)
        print(f"::set-output name=service_details::{json.dumps(service_details)}{os.linesep}")
        print(f"::set-output name=service_change_details::{json.dumps(service_change_details)}{os.linesep}")

    except Exception as e:
        print(f"::error ::{str(e)}{os.linesep}")
        raise e


if __name__ == "__main__":
    run_action()
