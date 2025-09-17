#!/bin/bash
NEXT_RELEASE_VERSION=$1
SIGNING_KEY=$2
git config --global user.name "tallulahh"
git config --global user.email "tallulah.carlisle@gmail.com"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global user.signingkey ${{ secrets.GPG_SIGNING_KEY }}
echo nextReleaseVersion=${nextRelease.version} >> build.env