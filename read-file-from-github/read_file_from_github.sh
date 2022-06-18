#!/bin/bash

fetch_file_contents() {

  # If the file is in the root of the repo, then filepath is empty and causes an extra '/' in the URL
  # git api responds with a 404 if this is the case. So compare file and if empty then construct URL without it
  if [[ -n "$FILEPATH" ]]
  then
    export fileUrl="$GITREPO/$GITREF/$FILEPATH/$FILENAME"
  else
    export fileUrl="$GITREPO/$GITREF/$FILENAME"
  fi

  fileContent=$(curl --header "Authorization: token $GHATOKEN" https://raw.githubusercontent.com/$fileUrl)
  printf "%s" "${fileContent}"
}

fetch_file_contents
