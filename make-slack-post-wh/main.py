import json
import os

from slack_post_to_webhook import PostToSlackWebhook


def main():
    slack_webhook_url = os.environ["INPUT_SLACK_WEBHOOK_URL"]
    if not slack_webhook_url.startswith("https://hooks.slack.com/services/"):
        raise Exception(f"[{slack_webhook_url}] is not a valid slack URL")

    action = os.environ["INPUT_ACTION"]
    action_success_str = os.environ["INPUT_ACTION_SUCCESS"]
    if action_success_str not in {"True", "False"}:
        raise Exception(f"[{action_success_str}] is not a valid value [True|False] for action_success")
    else:
        action_success = True if action_success_str == 'True' else False

    details_str = os.environ["INPUT_DETAILS"]
    if details_str != "":
        details = json.loads(details_str)
    else:
        details = None

    # Do the slack post
    post_slack = PostToSlackWebhook(slack_webhook_url, action, action_success, details)
    result = post_slack.post_to_webhook()
    print(f"::set-output name=result::{result}")


if __name__ == "__main__":
    main()
