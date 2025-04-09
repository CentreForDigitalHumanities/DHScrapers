FROM docker.io/library/python:3.12-slim
ENV PYTHONUNBUFFERED=1

COPY base_scraper /dh-scrapers/base_scraper
COPY utilities /dh-scrapers/utilities
RUN pip install --upgrade pip

WORKDIR /dh-scrapers
COPY requirements.txt /dh-scrapers/
RUN pip install -r requirements.txt