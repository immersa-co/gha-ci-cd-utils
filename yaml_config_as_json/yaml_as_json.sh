#!/bin/bash


fetch_yaml_as_json() {
  yamlcontent=$(curl --header "Authorization: token $GHATOKEN" https://raw.githubusercontent.com/$GITREPO/$GITREF/configs/$FILENAME.yaml)
  jsoncontent=$(echo "$yamlcontent" | sed '/#.*/d' | yq -o=json)
  if [[ $FILENAME == ci* ]]
  then
    jsoncontent=${jsoncontent//ci0x/$FILENAME} 
  fi
  printf "%s" "${jsoncontent}"
}

fetch_yaml_as_json
