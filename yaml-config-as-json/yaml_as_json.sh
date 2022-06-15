#!/bin/bash

export REPLACE_STR="ci0x"
fetch_multiple_yaml_as_json() {
  jsonKvs=''
  export kvs=$(echo $GITREPOS_REF_FILEPATH | jq 'to_entries[] | "\(.key):\(.value)"'  | tr "\n" " ")
  eval kvs_arr="($kvs)"
  for kv in "${kvs_arr[@]}"
  do
    key="${kv%:*}"
    repo_ref_filepath="${kv#*:}"
    jsonStr=$(fetch_yaml_as_json $repo_ref_filepath)
    jsonKvs+="\""$key"\":"$jsonStr","
  done
#  printf -v jsonArr "%s," "${jsonKvs[@]}"
  echo "{${jsonKvs%,}}"
#   echo "${jsonKvs[@]}"
}

fetch_yaml_as_json() {
  if [[ -z $1 ]]
  then
    repo_ref_filepath=$GITREPO_REF_FILEPATH
  else
    repo_ref_filepath=$1
  fi

  if [[ $FILENAME == ci* ]]
  then
    export readfile=$REPLACE_STR
  else
    export readfile=$FILENAME
  fi
  yamlcontent=$(curl --header "Authorization: token $GHATOKEN" https://raw.githubusercontent.com/$repo_ref_filepath/$readfile$FILEEXT)
  jsoncontent=$(echo "$yamlcontent" | sed '/#.*/d' | yq -o=json)
  if [[ $FILENAME == ci* ]]
  then
    jsoncontent=${jsoncontent//$REPLACE_STR/$FILENAME}
  fi
  printf "%s" "${jsoncontent}"
}

if [[ $GITREPO_REF_FILEPATH == "none" ]]
then
  fetch_multiple_yaml_as_json
else
  fetch_yaml_as_json "$GITREPO_REF_FILEPATH"
fi
