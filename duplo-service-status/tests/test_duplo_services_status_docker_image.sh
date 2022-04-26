export INPUT_HOST="https://immersa-dev.duplocloud.net/"
export INPUT_TENANT="dev01"
#export INPUT_TENANT_ID="ed684c6c-9876-4fde-999a-849d6586a4a7"
export INPUT_TOKEN=$duplo_dev_token
export INPUT_SERVICES='["all"]'
export INPUT_MAX_ATTEMPTS=5
export INPUT_RETRY_DELAY=1

image_tag='test:test-gha-duplo-services-status-v1'
docker build --platform linux/amd64 -t $image_tag ..
docker run -e INPUT_HOST -e INPUT_TENANT -e INPUT_TOKEN -e INPUT_SERVICES \
-e INPUT_MAX_ATTEMPTS -e INPUT_RETRY_DELAY -it --platform linux/amd64 $image_tag
