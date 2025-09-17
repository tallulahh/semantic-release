#!/bin/bash
git config --global user.name "tallulahh"
git config --global user.email "tallulah.carlisle@gmail.com"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global user.signingkey ${{ secrets.GPG_SIGNING_KEY }}
echo nextReleaseVersion=${nextRelease.version} >> build.env