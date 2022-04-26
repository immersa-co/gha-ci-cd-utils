export INPUT_HOST="https://immersa-dev.duplocloud.net/"
export INPUT_TENANT="dev01"
export INPUT_TOKEN=$duplo_dev_token
export INPUT_SERVICES='["api", "btcs", "ftcs"]'

python3 ../duplo_services_details.py

export INPUT_SERVICES='["all"]'
python3 ../duplo_services_details.py

export INPUT_SERVICES='["i-donot-exist"]'
python3 ../duplo_services_details.py
