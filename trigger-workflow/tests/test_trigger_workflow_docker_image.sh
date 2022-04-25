export github_app_id=$github_app_id_w
export github_app_key=$github_app_key_w
export github_install_id=$github_install_id_w

export INPUT_GHA_TOKEN="$(python3 ~/utils/generateGithubAppToken.py)"
export INPUT_GITHUB_REPO="immersa-co/change-control-manager"
export INPUT_WORKFLOW_NAME='deploy-setup.yaml'
export INPUT_WORKFLOW_REF='main'
export INPUT_INPUTS=''

image_tag='test:test-gha-trigger_workflow-v1'
docker build --platform linux/amd64 -t $image_tag ..
docker run -e INPUT_GHA_TOKEN -e INPUT_GITHUB_REPO -e INPUT_WORKFLOW_NAME \
-e INPUT_WORKFLOW_REF -e INPUT_INPUTS -it --platform linux/amd64 $image_tag
