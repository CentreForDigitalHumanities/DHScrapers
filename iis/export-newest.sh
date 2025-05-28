#!/bin/bash
mkdir /iis-harvester-data/harvest-metadata
mkdir /iis-harvester-data/iis-files
git fetch
export FILE="/iis-harvester-data/harvest-metadata/harvested-files.txt"
git status --porcelain epidoc-files > $FILE
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
    mv epidoc-files/*.xml /iis-harvester-data/iis-files/
fi
