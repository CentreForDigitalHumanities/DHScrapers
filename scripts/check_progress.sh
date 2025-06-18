#!/bin/bash
# compare the output and postprocessed directories
export TIMESTAMP=$(date +%Y%m%d_%H%M%S)
echo $TIMESTAMP
cd /output
ls *.xml > /metadata/enriched.txt
cd /postprocessed
ls *.xml > /metadata/postprocessed.txt
comm -12 /metadata/enriched.txt /metadata/postprocessed.txt > /metadata/finished.txt
FILE_LENGTH=$(wc -l </metadata/finished.txt)
if [ "$FILE_LENGTH" -gt 0 ]; then
    # move all files that are shared between output and postprocessed to a timestamped subdirectory
    mkdir /output/$TIMESTAMP
    cd /output
    for file in $(cat /metadata/finished.txt); do mv "$file" /output/$TIMESTAMP; done
    # now in the next step, only files which haven't been postprocessed yet will be in the /output root directory
fi