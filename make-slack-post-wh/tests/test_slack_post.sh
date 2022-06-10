export INPUT_SLACK_WEBHOOK_URL="$(cat ~/utils/slackurl)"
export INPUT_ACTION="testing github action step"
export INPUT_DETAILS=''
export INPUT_ACTION_DESCRIPTION=""

export INPUT_ACTION_SUCCESS="true"
python3 ../slack_post_via_webhook.py

export INPUT_ACTION_SUCCESS="starting"
python3 ../slack_post_via_webhook.py

export INPUT_DETAILS='{"Repo":"https://github.com/imsurat/gha-ci-cd-utils/", "Github Run" : "https://github.com/imsurat/gha-ci-cd-utils//actions/runs/6138234562"}'
export INPUT_ACTION_SUCCESS="True"
export INPUT_ACTION_DESCRIPTION="Running \`['api:dev-215c369-105', 'btcs:develop-ba3b2f0-41', 'ftcs:main-e0419a1-13']\`"

python3 ../slack_post_via_webhook.py


export INPUT_DETAILS='{"Repo":"https://github.com/imsurat/gha-ci-cd-utils/", "Github Run" : "https://github.com/imsurat/gha-ci-cd-utils//actions/runs/6138234562"}'
export INPUT_ACTION_SUCCESS="False"
export INPUT_ACTION_DESCRIPTION="Running \`['api:dev-215c369-105', 'btcs:develop-ba3b2f0-41', 'ftcs:main-e0419a1-13']\`"

python3 ../slack_post_via_webhook.py
