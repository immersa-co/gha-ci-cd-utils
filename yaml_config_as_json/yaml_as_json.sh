#!/bin/bash


fetch_yaml_as_json() {

  if [[ $FILENAME == ci* ]]
  then
    export readfile="ci0x"
  else
    export readfile=$FILENAME
  fi
  yamlcontent=$(curl --header "Authorization: token $GHATOKEN" https://raw.githubusercontent.com/$GITREPO/$GITREF/$FILEPATH/$readfile$FILEEXT)
  jsoncontent=$(echo "$yamlcontent" | sed '/#.*/d' | yq -o=json)
  if [[ $FILENAME == ci* ]]
  then
    jsoncontent=${jsoncontent//ci0x/$FILENAME} 
  fi
  printf "%s" "${jsoncontent}"
}

fetch_yaml_as_json
