export INPUT_HOST="https://immersa-dev.duplocloud.net/"
export INPUT_TENANT="dev01"
export INPUT_TOKEN=$duplo_dev_token
export INPUT_SERVICES='["api", "btcs", "ftcs"]'
export INPUT_MAX_ATTEMPTS=5
export INPUT_RETRY_DELAY=1

python3 ../duplo_services_status.py

#export INPUT_SERVICES='["i-donot-exist"]'
#python3 ../duplo_services_status.py
#
export INPUT_SERVICES='["all"]'
python3 ../duplo_services_status.py
#
#export INPUT_SERVICES=''
#python3 ../duplo_services_status.py
