import os
import sys
import logging
from goodreads.constants import EDITION_LANGUAGES
from goodreads.edition_scraper import scraper as editions_scraper
from goodreads.review_scraper import scraper as review_scraper

logger = logging.getLogger(__name__)


def scrape(
        editions_url, 
        export_folder, 
        edition_languages = EDITION_LANGUAGES, 
        editions_csv_filename = None, 
        reviews_csv_filename = 'reviews.csv', 
        export_xml = False, 
        export_txt = False
    ):
    '''
    Non-commandline entry point for the module. For full documentation of the parameters please refer to `__main__.py`,
    command line help, or the module's README.
    '''       
    editions = editions_scraper.scrape(editions_url, export_folder, editions_csv_filename)
    review_scraper.scrape(editions, export_folder, reviews_csv_filename, export_xml, export_txt, edition_languages)
    logger.info('Done')
