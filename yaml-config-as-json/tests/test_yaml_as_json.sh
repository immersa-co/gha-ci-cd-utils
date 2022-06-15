export github_app_key=$github_app_key_ro
export github_app_id=$github_app_id_ro
export github_install_id=$github_install_id_ro

export FILEEXT=".yaml"
export GHATOKEN="$(python3 ~/utils/generateGithubAppToken.py)"

export GITREPO_REF_FILEPATH="immersa-co/api/main/configs"
export GITREPOS_REF_FILEPATH="none"

export FILENAME="dev01"
../yaml_as_json.sh

export GITREPO_REF_FILEPATH="immersa-co/api/add-ci-configs/configs"
export FILENAME="ci01"
../yaml_as_json.sh

export GITREPO_REF_FILEPATH="none"
export GITREPOS_REF_FILEPATH='{"api":"immersa-co/api/main/configs", "btcs":"immersa-co/btcs/main/configs"}'

export FILENAME="dev01"
../yaml_as_json.sh

export GITREPOS_REF_FILEPATH='{"api":"immersa-co/api/add-ci-configs/configs", "btcs":"immersa-co/btcs/add-ci-configs/configs"}'
export FILENAME="ci01"
../yaml_as_json.sh
