#!/bin/bash

process_commit_steps() {
  # Get current contents and sha of the file
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
  currentContentEncoded=$(echo $gitContents | jq '.content' | tr -d '"' | sed 's/\\n//g')
  currentSha=$(echo $gitContents | jq '.sha' | tr -d '"')
  echo "$gitContents"
  # Base 64 encode the desired contents and compare with what is in repo. If same then return the commit-sha of
  # head otherwise commit and return the sha. the only way to make encode/decode work reliably across testing locally
  # on MAC and the actual github action is to use the -w 0 flag on Linux and not use on MAC
  fileContentBase64=$(echo "$FILECONTENTS" | base64 $BASE64OPTIONS)

  if [[ "$currentContentEncoded" == "$fileContentBase64" ]]
  then
    # Get the commit sha of the tree
    repoRefResponse=$(curl -H "Accept: application/vnd.github.v3+json" -H "Authorization: token $GHATOKEN" \
        https://api.github.com/repos/$GITREPO/git/ref/heads/$GITBRANCH)
    COMMIT_SHA=$(echo $repoRefResponse | jq '.object.sha' | tr -d '"')
    FILE_UPDATED='False'
    echo "$repoRefResponse"
  else
    # Make a commit to the branch
    response=$(curl -X PUT -H "Accept: application/vnd.github.v3+json" -H "Authorization: token $GHATOKEN" \
      -d "{\"message\": \"$MESSAGE\", \"content\": \"$fileContentBase64\", \"sha\": \"$currentSha\", \"branch\" : \"$GITBRANCH\"}" \
       https://api.github.com/repos/$fileUrl)
    COMMIT_SHA=$(echo $response | jq '.commit.sha' | tr -d '"')
    FILE_UPDATED='True'
    echo "$response"
  fi

  echo "::set-output name=commitSha::$(echo $COMMIT_SHA)"
  echo "::set-output name=updated::$(echo $FILE_UPDATED)"
}

process_commit_steps
