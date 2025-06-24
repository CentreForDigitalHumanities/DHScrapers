#!/bin/sh
cp -r /epidoc-repo /epidoc/stylesheets
export FILE="/harvest-metadata/inprogress.txt"
if [ -f "$FILE" ]; then
    exit 0
fi
cp -r /iis-repo /iis-files/originals
cd /iis-files/originals
git fetch
git status --porcelain epidoc-files > $FILE
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
fi
