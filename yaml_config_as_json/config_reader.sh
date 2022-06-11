#!/bin/bash

timestamp() {
  date +"%s"
}


fetch_service_config_4_tenant() {
  yamlconfig=$(curl --header "Authorization: token $GHATOKEN" https://raw.githubusercontent.com/$SERVICEREPO/$CONFIGREF/configs/$TENANTNAME.yaml)
  jsonconfig=$(echo $yamlconfig | yq r -j)
  printf "%s" "${jsonconfig}"
}

fetch_gha_token


#            repo = service_data["repository"]
#            ref = service_data["config-ref"]
#            url = f"https://api.github.com/repos/{repo}/contents/configs/{self.duplo_tenant}.yaml?ref={ref}"
#            headers = {"Authorization": f"token {self.gha_token}", "Accept": "application/vnd.github.v3.raw"}
#            response = requests.get(url, headers=headers)
