#!/bin/sh
mkdir /current_run/harvest-metadata
mkdir /current_run/iis-files
git fetch
export FILE="/current_run/harvest-metadata/harvested-files.txt"
git status --porcelain epidoc-files > $FILE
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
    mv epidoc-files/*.xml /current_run/iis-files/
fi
