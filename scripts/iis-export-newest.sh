#!/bin/sh
export FILE="/harvest-metadata/inprogress.txt"
# check if inprogress.txt still exits, if so: skip the rest of this script
if [ -f "$FILE" ]; then
    exit 0
fi
# download epidoc files from git, if this hasn't been done yet
cd /epidoc
if [ ! -d stylesheets ]; then
    # clone the epidoc repository
    git clone -b v9.5 --single-branch https://github.com/EpiDoc/Stylesheets stylesheets
fi
cd /iis-files
# clone iip-texts repository from git, if this hasn't been done yet
if [ ! -d originals ]; then
    git clone -n --depth=1 --filter=tree:0 https://github.com/Brown-University-Library/iip-texts/ originals
    cd originals
    # check out only the /epidoc-files directory
    git sparse-checkout set --no-cone /epidoc-files
    cd ..
fi
# check if there are differences on the remote since the last run
git status --porcelain epidoc-files > $FILE
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
fi
