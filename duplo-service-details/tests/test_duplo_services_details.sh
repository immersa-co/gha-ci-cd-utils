export INPUT_HOST="https://immersa-dev.duplocloud.net/"
export INPUT_TENANT="dev01"
export INPUT_TOKEN=$duplo_dev_token

export INPUT_SERVICES='["api", "btcs", "ftcs"]'
export INPUT_FILTER_TAGS='["main", "hotfix"]'
python3 ../duplo_services_details.py

export INPUT_SERVICES='["api", "btcs", "ftcs"]'
export INPUT_FILTER_TAGS=''
python3 ../duplo_services_details.py

export INPUT_SERVICES='["all"]'
export INPUT_FILTER_TAGS='["main", "hotfix"]'
python3 ../duplo_services_details.py

export INPUT_SERVICES='["all"]'
export INPUT_FILTER_TAGS=''
python3 ../duplo_services_details.py

export INPUT_SERVICES='["i-donot-exist"]'
export INPUT_FILTER_TAGS='["main", "hotfix"]'
python3 ../duplo_services_details.py

export INPUT_SERVICES='["i-donot-exist"]'
export INPUT_FILTER_TAGS=''
python3 ../duplo_services_details.py
