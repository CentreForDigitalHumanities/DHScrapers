#!/bin/sh
git fetch
export FILE="/harvest-metadata/harvested-files.txt"
git status --porcelain epidoc-files > $FILE
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
    cp epidoc-files/*.xml /iis-files/
fi
