#!/bin/bash
NEXT_RELEASE_VERSION=$1
SIGNING_KEY=$2
git config --global user.name "tallulahh"
git config --global user.email "tallulah.carlisle@gmail.com"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global user.signingkey $SIGNING_KEY
git config --global push.gpgsign true
echo nextReleaseVersion=$NEXT_RELEASE_VERSION >> build.env
