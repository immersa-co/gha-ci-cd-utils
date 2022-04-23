export INPUT_SLACK_WEBHOOK_URL="$(cat ~/utils/slackurl)"
export INPUT_ACTION="testing github action step"
export INPUT_DETAILS='{"Repo":"https://github.com/imsurat/gha-ci-cd-utils/", "Github Run" : "https://github.com/imsurat/gha-ci-cd-utils//actions/runs/6138234562"}'

export INPUT_ACTION_SUCCESS="True"
python3 ../main.py

export INPUT_ACTION_SUCCESS="False"
python3 ../main.py
