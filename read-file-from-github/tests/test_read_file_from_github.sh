export github_app_key=$github_app_key_ro
export github_app_id=$github_app_id_ro
export github_install_id=$github_install_id_ro

export GHATOKEN="$(python3 ~/utils/generateGithubAppToken.py)"

export GITREPO="immersa-co/api"
export GITREF="main"
export FILEPATH="configs"

export FILENAME="dev01.yaml"
../read_file_from_github.sh
