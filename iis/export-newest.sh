#!/bin/bash
git fetch
export FILE="/output/changed.txt"
git status --porcelain epidoc-files > /output/changed.txt
FILE_LENGTH=$(wc -l <"$FILE")
if [ "$FILE_LENGTH" -gt 0 ]; then
    git checkout
fi
