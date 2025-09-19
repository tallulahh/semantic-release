NEXT_RELEASE=$1
echo nextReleaseVersion=$NEXT_RELEASE >> build.env
python3 ./scripts/update_readme.py