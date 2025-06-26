FROM docker.io/library/python:alpine

RUN apk add --no-cache git

ENV PYTHONUNBUFFERED=1

# equals a mkdir and a cd
WORKDIR /dh-scrapers

COPY ./base_scraper ./base_scraper
COPY ./utilities ./utilities
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# to fix the urllib3 version error (see: https://stackoverflow.com/questions/78163280/no-module-named-urllib3-packages-six-moves)
RUN pip install requests --upgrade && pip install urllib3 --upgrade

COPY ./scripts ./scripts

# copy python module for iis scraper
COPY ./iis /dh-scrapers/iis
RUN chmod -R g+rwx /dh-scrapers # rootless