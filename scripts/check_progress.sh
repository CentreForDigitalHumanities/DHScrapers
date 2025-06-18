#!/bin/bash
# compare the output and postprocessed directories
export $TIMESTAMP=(%Y%m%d_%H%M%S)
cd /output/inprogress/
ls *.xml > ~/enriched.txt
cd /postprocessed/inprogress
ls *.xml > ~/postprocessed.txt
comm -12 ~/enriched.txt ~/postprocessed.txt > ~/finished.txt
# move all files that are shared between output and postprocessed to $JOB-finished
mkdir /output/$TIMESTAMP
cd /output/inprogress/
for file in $(cat ~/finished.txt); do mv "$file" /output/$TIMESTAMP; done
# now in the next step, only files which haven't been postprocessed yet will be in the /output/inprogress directory