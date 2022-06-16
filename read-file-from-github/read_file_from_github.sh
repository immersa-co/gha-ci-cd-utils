#!/bin/bash

fetch_file_contents() {
  fileContent=$(curl --header "Authorization: token $GHATOKEN" https://raw.githubusercontent.com/$GITREPO/$GITREF/$FILEPATH/$FILENAME)
  printf "%s" "${fileContent}"
}

fetch_file_contents
