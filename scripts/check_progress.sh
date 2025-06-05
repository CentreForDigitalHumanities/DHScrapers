#!/bin/bash
# compare the output and postprocessed directories
cd /output/$JOB/
ls *.xml > ~/enriched.txt
cd /postprocessed/$JOB
ls *.xml > ~/postprocessed.txt
comm -12 ~/enriched.txt ~/postprocessed.txt > ~/finished.txt
# move all files that are shared between output and postprocessed to $JOB-finished
mkdir /output/$JOB-finished
cd /output/$JOB
for file in $(cat ~/finished.txt); do mv "$file" /output/$JOB-finished; done
# now in the next step, only files which haven't been postprocessed yet will be in the /output/$JOB directory