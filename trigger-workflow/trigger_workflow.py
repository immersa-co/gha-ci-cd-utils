import json
import os

from github import Github


def run_action() -> None:
    # github_token, github_repo, workflow_name, workflow_version
    github_app_token = os.environ["INPUT_GHA_TOKEN"]
    github_repo = os.environ["INPUT_GITHUB_REPO"]
    workflow_name = os.environ["INPUT_WORKFLOW_NAME"]
    workflow_ref = os.environ["INPUT_WORKFLOW_REF"]
    inputs = os.environ["INPUT_INPUTS"]

    try:
        if workflow_ref is None or workflow_ref == '':
            workflow_ref = "main"
        github_api = Github(github_app_token)
        github_repo = github_api.get_repo(github_repo)
        workflow = github_repo.get_workflow(workflow_name)
        if inputs == '':
            result = workflow.create_dispatch(workflow_ref)
        else:
            inputs_dict = json.loads(inputs)
            result = workflow.create_dispatch(workflow_ref, inputs=inputs_dict)
        print(f"::set-output name=result::{result}{os.linesep}")
    except Exception as e:
        print(f"::error ::{str(e)}{os.linesep}")
        raise e


if __name__ == "__main__":
    run_action()
