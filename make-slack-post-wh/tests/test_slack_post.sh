export INPUT_SLACK_WEBHOOK_URL="$(cat ~/utils/slackurl)"
export INPUT_ACTION="testing github action step"
export INPUT_DETAILS=""

export INPUT_ACTION_SUCCESS="True"
python3 ../main.py

export INPUT_ACTION_SUCCESS="False"
python3 ../main.py
