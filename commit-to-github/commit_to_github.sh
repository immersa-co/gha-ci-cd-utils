#!/bin/bash

get_current_contents() {
  if [[ -n "$FILEPATH" ]]
  then
    # If the file is in the root of the repo, then filepath is empty and causes an extra '/' in the URL
    # git api responds with a 404 if this is the case. So compare file and if empty then construct URL without it
    export fileUrl="$GITREPO/contents/$FILEPATH/$FILENAME"
  else
    export fileUrl="$GITREPO/contents/$FILENAME"
  fi
   # it took quite some time to get this working with stripping "\n" in the encoded contents. tr -d '\\n'
   # does not work, sed does. Using "Accept: application/vnd.github.VERSION.raw" will give un-encoded contents
  gitContents=$(curl -H "Accept: application/vnd.github.v3+json" -H "Authorization: token $GHATOKEN" \
                 https://api.github.com/repos/$fileUrl?ref=$GITBRANCH)
  export currentContent=$(echo $gitContents | jq '.content' | tr -d '"' | sed 's/\\n//g')
  export currentSha=$(echo $gitContents | jq '.sha' | tr -d '"')
}

process_commit_steps() {
  # Get current contents and sha of the file
  get_current_contents
  # BAse 64 encode the desired contents and compare with what is in repo. If same then return the commit-sha of
  # head otherwise commit and return the sha
  fileContentBase64=$(echo "$FILECONTENTS" | base64)
  if [[ "$currentContent" == "$fileContentBase64" ]]
  then
    # Get the commit sha of the tree
    repoRefResponse=$(curl -H "Accept: application/vnd.github.v3+json" -H "Authorization: token $GHATOKEN" \
        https://api.github.com/repos/$GITREPO/git/ref/heads/$GITBRANCH)
    echo $repoRefResponse | jq '.object.sha'
    export FILE_UPDATED='False'
  else
    # Make a commit to the branch
    response=$(curl -X PUT -H "Accept: application/vnd.github.v3+json" -H "Authorization: token $GHATOKEN" \
      -d "{\"message\": \"$MESSAGE\", \"content\": \"$fileContentBase64\", \"sha\": \"$currentSha\", \"branch\" : \"$GITBRANCH\"}" \
       https://api.github.com/repos/$fileUrl)
    echo $response | jq '.commit.sha' | tr -d '"'
    export FILE_UPDATED='True'
  fi
}

commitSha=$(process_commit_steps)
echo "::set-output name=commitSha::$commitSha"
echo "::set-output name=updated::$FILE_UPDATED"
