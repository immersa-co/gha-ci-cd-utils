import json
import os
import requests


class PostToSlackWebhook:
    def __init__(self, slack_webhook_url, action, action_success, starting_action, details=None, action_description=None):
        self.slack_webhook_url = slack_webhook_url
        self.action = action
        self.action_success = action_success
        self.starting_action = starting_action
        self.details = details
        self.action_description = action_description

    @staticmethod
    def get_slack_payload_section(about, url):
        return \
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f":point_right: To see more about the {about}."},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": f"Go to {about}", "emoji": True},
                    "url": url,
                    "action_id": "button-action"
                }
            }

    def get_slack_payload_status_text(self):
        if self.starting_action:
            text = f":large_orange_circle: Starting {self.action}"
        else:
            success_text = f":tada: The {self.action} was successfully completed"
            failure_text = f":alert: The {self.action} could not be successfully completed"
            text = success_text if self.action_success else failure_text
            text = f"{text}. {self.action_description}"
        return text

    def get_slack_payload(self):
        text = self.get_slack_payload_status_text()
        if self.details is not None:
            blocks_array = [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]
            for about in self.details:
                blocks_array.append(PostToSlackWebhook.get_slack_payload_section(about, self.details[about]))
            # text element is what shows up in the desktop notification
            # block is the message posted on the channel
            payload_json = {
                "text": text,
                "blocks":  blocks_array
            }
        else:
            payload_json = {
                "text": text,
            }
        return json.dumps(payload_json).encode("utf-8")

    def post_to_webhook(self):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(self.slack_webhook_url, headers=headers, data=self.get_slack_payload())

        if not response.ok:
            message = f"Failed to post {self.action} with result[ {self.action_success}] to slack [{response.content}]"
            print(message)
            return False
        else:
            return True


def main():
    slack_webhook_url = os.environ["INPUT_SLACK_WEBHOOK_URL"]
    if not slack_webhook_url.startswith("https://hooks.slack.com/services/"):
        raise Exception(f"[{slack_webhook_url}] is not a valid slack URL")

    starting_action = False
    action = os.environ["INPUT_ACTION"]
    action_success_str = os.environ["INPUT_ACTION_SUCCESS"].lower()

    if action_success_str == "starting":
        starting_action = True
        action_success = None
    elif action_success_str not in {"true", "false"}:
        raise Exception(f"[{action_success_str}] is not a valid value [True|False|Starting] for action_success")
    else:
        action_success = True if action_success_str == 'true' else False

    details_str = os.environ["INPUT_DETAILS"]
    if details_str != "":
        details = json.loads(details_str)
    else:
        details = None

    action_description = os.environ["INPUT_ACTION_DESCRIPTION"]
    if action_description == "":
        action_description = None
    # Do the slack post
    post_slack = PostToSlackWebhook(slack_webhook_url, action, action_success, starting_action,
                                    details, action_description)
    result = post_slack.post_to_webhook()
    print(f"::set-output name=result::{result}{os.linesep}")


if __name__ == "__main__":
    main()
