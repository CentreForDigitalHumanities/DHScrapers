#!/bin/bash
# compare the output and postprocessed directories
export TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cd /output
# check if there are unprocessed files in output folder
if find . -type f -name "*.xml" | grep -q .; then
    ls *.xml > /metadata/enriched.txt
else
    exit 0 # if not, skip this step
fi
cd /postprocessed
# check if there are already xml files in the postprocessed folder
if find . -type f -name "*.xml" | grep -q .; then
    ls *.xml > /metadata/postprocessed.txt # if so, write them out
else
    exit 0 # otherwise, skip this step until the next run
fi
comm -12 /metadata/enriched.txt /metadata/postprocessed.txt > /metadata/finished.txt
FILE_LENGTH=$(wc -l </metadata/finished.txt)
if [ "$FILE_LENGTH" -gt 0 ]; then
    # move all files that are shared between output and postprocessed to a timestamped subdirectory
    mkdir /output/$TIMESTAMP
    cd /output
    for file in $(cat /metadata/finished.txt); do mv "$file" /output/$TIMESTAMP; done
    # now in the next step, only files which haven't been postprocessed yet will be in the /output root directory
fi