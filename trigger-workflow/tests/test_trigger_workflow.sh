export github_app_id=$github_app_id_w
export github_app_key=$github_app_key_w
export github_install_id=$github_install_id_w

export INPUT_GHA_TOKEN="$(python3 ~/utils/generateGithubAppToken.py)"
export INPUT_GITHUB_REPO="immersa-co/change-control-manager"
export INPUT_WORKFLOW_NAME='promote_service_image.yaml'
export INPUT_WORKFLOW_REF='main'
export INPUT_INPUTS='{"service":"api"}'

python3 ../trigger_workflow.py
