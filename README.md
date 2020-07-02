# dhlab-scrapers

This repo attempts to collect various scrapers developed by the Digital Humanities Lab into one place, and create some re-usable base code in the process. As such, it is an attempt to make life easier for future developers that need to do some scraping (quickly). The idea is that each specific scraper becomes its own module, with classes in it that inherit from the base classes.

## Installation

Make sure you have Python3 installed (any version should do, tested with 3.6) and create a virtualenv. There are two ways to install, and it depend on which scraper you intend to use which option you need. If the scraper you wnat to use does not have a `requirements.txt` in the module, the general dependencies will do. In this case, just run `pip install -r requirements.txt` from the prioject root folder.

In the other case, do the equivalent of `pip install -r iis/requirement.txt`, where `iis` is the name of the module (i.e. scraper) you want to use.

Once this is done, start the virtualenv, and you're good to go!

## Overview

### Scraper

Scraping stuff from the web is divided into three (optional) steps by this module:

1. COLLECT the html from a webpage
2. PARSE the html into entities, i.e. extract the info we need
3. EXPORT these entities into the format(s) we want

These steps translate into the three respective base classes. In addition, there is the idea of a `base_entity` and some children of that (`book_edition` and `book_review` at the time of writing). These allow us to present the info that we extracted from any html in a uniform way to the exporter.

### General

Calling a specific scraper should be as easy as `python -m goodreads --whatever_args_we_expect`. Therefore, any new module should have a `__main__py` entrypoint. If the scraper should be re-usable, it might be nice to create a neat command line interface for it here. Next to `__main__.py` should be a script that is the main entrypoint for non-commandline use (e.g. `goodreads.py`). This script can be as simple or as complex as you want. It could implement the steps described above directly, or import them from other scripts.

### Base classes

| class | features |
| ----- | ----- |
| collector | handle actual requests, some url utility functions |
| parser | create BeautifulSoup and GenderDetector instances, some whitespace utility functions |
| exporter | export collected entities into different formats (CSV, TXT, XML)

### Entities

Typically, we either need the entire page, for example when each page is a data instance (e.g. each page is XML containing one entity / instance), or we need to parse the HTML to extract the info we need. For the second case, this module offers base entities, the most important feature of which is uniformization to enable re-usablility of the exporter class.

The important thing with entities is that they will be translated into `dict`s. By default, `to_dict()` returns the output of `vars()` (which calls `__dict__` underwater). If need be, this can be customized by overwriting `to_dict`, for example if one of the field values needs to be calculated on the basis of others, or the specific formatting is required.

Tip: the order of fields in the export(s) can be influenced by listing the fields of the entity in the class' constructor in the desired order (see `goodreads.entities.review.py` for an example).

## Utilities / Logging

There is currently one utility in the utilities module: an initializer for a logger. Calling this function will give you a logger that will log INFO (and above) to the console, and DEBUG and above a file. Simply call this function before doing anything else, and you can import the logger (`logger = logging.getLogger(__name__)`) in each script (`parser`, `collector`, etc) and start logging.
