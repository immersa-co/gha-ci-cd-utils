export INPUT_HOST="https://immersa-dev.duplocloud.net/"
export INPUT_TENANT="dev01"
export INPUT_TENANT_ID="ed684c6c-9876-4fde-999a-849d6586a4a7"
export INPUT_TOKEN=$duplo_dev_token
export INPUT_SERVICES='["all"]'

python3 ../duplo_services_status.py
