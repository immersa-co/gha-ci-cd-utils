export github_app_key=$github_app_key_w
export github_app_id=$github_app_id_w
export github_install_id=$github_install_id_w

export GHATOKEN="$(python3 ~/utils/generateGithubAppToken.py)"

export GITREPO="immersa-co/change-control"
export GITBRANCH="setup"
export FILEPATH=""
export FILENAME="services.yaml"
export MESSAGE="Updating service.yaml to test"

export FILECONTENTS=$(curl --header "Authorization: token $GHATOKEN" https://raw.githubusercontent.com/$GITREPO/$GITBRANCH/$FILENAME)

../commit_to_github.sh
