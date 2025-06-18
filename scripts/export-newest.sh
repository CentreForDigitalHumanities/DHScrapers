#!/bin/sh
git fetch
export FILE="/harvest-metadata/inprogress.txt"
git status --porcelain epidoc-files > $FILE
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
    mv *.xml /iis-files/inprogress
fi
