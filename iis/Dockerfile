FROM docker.io/library/alpine:3

RUN apk add --no-cache git

WORKDIR /epidoc-stylesheets
RUN git clone https://github.com/EpiDoc/Stylesheets .

WORKDIR /iis-files 
RUN git clone -n --depth=1 --filter=tree:0 \
    https://github.com/Brown-University-Library/iip-texts/ .
# check out only the /epidoc-files directory
RUN git sparse-checkout set --no-cone /epidoc-files
COPY export-newest.sh /scripts/
