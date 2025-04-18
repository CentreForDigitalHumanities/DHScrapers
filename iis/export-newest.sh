#!/bin/bash
git fetch
export FILE="/harvest-metadata/$JOB.txt"
git status --porcelain epidoc-files > $FILE
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
    mv *.xml /iis-files/$JOB
fi
