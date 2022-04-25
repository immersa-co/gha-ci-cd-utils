export INPUT_SLACK_WEBHOOK_URL="$(cat ~/utils/slackurl)"
export INPUT_ACTION="testing github action step"
export INPUT_ACTION_SUCCESS="True"
export INPUT_DETAILS=""

image_tag='test:test-gha-slack-v1'
docker build --platform linux/amd64 -t $image_tag ..
docker run -e INPUT_SLACK_WEBHOOK_URL -e INPUT_ACTION -e INPUT_ACTION_SUCCESS \
-e INPUT_DETAILS -it --platform linux/amd64 $image_tag

export INPUT_ACTION_SUCCESS="False"
export INPUT_DETAILS='{"Repo":"https://github.com/imsurat/gha-ci-cd-utils/", "Github Run" : "https://github.com/imsurat/gha-ci-cd-utils//actions/runs/6138234562"}'
docker run -e INPUT_SLACK_WEBHOOK_URL -e INPUT_ACTION -e INPUT_ACTION_SUCCESS \
-e INPUT_DETAILS -it --platform linux/amd64 $image_tag
