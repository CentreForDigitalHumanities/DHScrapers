#!/bin/bash
git fetch
export FILE="/harvest-metadata/harvested-files.txt"
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    exit 0 #! there are still unprocessed files, complete the job and continue to next job
fi
git status --porcelain epidoc-files > /harvest-metadata/harvested-files.txt
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
fi
