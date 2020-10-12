import sys
import requests
import json
import time
import logging
from base_scraper.collector import Collector as BaseCollector
from .parser import ReviewPageParser

logger = logging.getLogger(__name__)
# example_of_full_url: 'https://www.goodreads.com/book/reviews/15797938-the-dinner?edition_reviews=true&rating=5&text_only=true&page=10'


def collect(edition, min_review_length = 6, metadata = {}, max_reviews = 100):
    '''
    Collect as many reviews as we can for edition.

    Parameters:
        edition -- An instance of Edition.
        min_review_length -- the minimum length of a single review (in characters). 
            Reviews shorter than this will be excluded. Defaults to 6.
        metadata - a dict of pairs (i.e fieldname, value) to add to each review.
            Is empty by default.
    '''
    if not edition:
        raise ValueError('edition cannot be None or empty')

    collector = GoodReadsReviewCollector(edition, min_review_length, metadata, max_reviews)
    reviews = []
    first_page_parser = collector.get_page_parser(1)
    number_of_reviews = first_page_parser.get_number_of_text_only_reviews()

    if number_of_reviews == max_reviews:
        logger.info("More than " + str(max_reviews) + " reviews found, collecting per rating.")
        reviews = collector.collect_per_rating()
    else:
        reviews = collector.collect_non_top_X(first_page_parser)
    return reviews


class GoodReadsReviewCollector(BaseCollector):

    def __init__(self, edition, min_review_length = 6, metadata = {}, max_reviews = 100):
        '''
        edition - the edition these reviews belong to
        min_review_length - the minimum length of a single review (in characters). 
            Reviews shorter than this will be excluded. Defaults to 6.
        metadata - a dict of pairs (i.e fieldname, value) to add to each review.
            Is empty by default.
        '''
        self.base_url = 'https://www.goodreads.com/book/reviews/'
        self.edition = edition
        self.min_review_length = min_review_length
        self.metadata = metadata
        self.max_reviews = max_reviews

    def collect_per_rating(self):
        '''
        Collect the reviews for edition on a per rating basis.
        '''
        reviews = []
        for rating in range(1, 6):
            first_page_parser = self.get_page_parser(1, rating)
            number_of_reviews = first_page_parser.get_number_of_text_only_reviews()
            if number_of_reviews == self.max_reviews:
                reviews.extend(self.collect_top_X(first_page_parser, rating))
            else:
                reviews.extend(self.collect_non_top_X(first_page_parser, rating))
        return reviews

    def collect_non_top_X(self, first_page_parser, rating=None):
        '''
        Collect all pages of reviews for a limited (i.e. not top 100) set.
        '''
        reviews = []
        number_of_reviews = first_page_parser.get_number_of_text_only_reviews()
        reviews.extend(first_page_parser.get_reviews())
        if first_page_parser.contains_only_reviews():
            number_of_pages = self.get_number_of_pages(number_of_reviews, 30)
            for page_number in range(2, number_of_pages + 1):
                parser = self.get_page_parser(page_number, rating, True)
                reviews.extend(parser.get_reviews())
        return reviews

    def collect_top_X(self, first_page_parser, rating):
        '''
        (Naively) Collect 10 pages of 30 text_only reviews.
        '''
        reviews = first_page_parser.get_reviews()
        for page_number in range(2, 11):
            parser = self.get_page_parser(page_number, rating)
            reviews.extend(parser.get_reviews())
        return reviews

    def get_page_parser(self, page_number, rating=None, text_only=False):
        '''
        Get an instance of ReviewPageParser with the requested page loaded.
        '''
        page_url = self.get_page_url(page_number, rating, text_only)
        self.log_collection_details(page_number, rating)
        html = self.parse_response(self.collect_html(page_url))
        return ReviewPageParser(html, self.edition, self.min_review_length, self.metadata, self.max_reviews)

    def get_page_url(self, page_number, rating=None, text_only=False):
        '''
        Extend base url with edition id and a query.
        Note that 'text_only=true' will always be added when page_number is 1, because
        the first page collected is used to establish how many reviews we are dealing with.

        Parameters
            text_only -- Add the 'text_only=True' query param. Defaults to False.
        '''
        url = "{}{}?edition_reviews=true".format(self.base_url, self.edition.get_id())
        if rating:
            url = "{}&rating={}".format(url, rating)
        if text_only or page_number == 1:
            url = "{}&text_only=true".format(url)
        url = "{}&page={}".format(url, page_number)
        return url

    def parse_response(self, response_text):
        '''
        Strips some javascript surrounding the HTML, converts unicode characters, 
        replaces newlines and HTML encoded apostrophes.
        Should do the trick in most cases.
        '''
        # strip javascript
        unicode_html = response_text[26:-2]
        return json.loads(unicode_html).replace("\n", "").replace("&#39;", "'")

    def log_collection_details(self, page_number, rating=None, text_only=False):
        '''
        Log what we are collecting with some detail
        '''
        message = "  Collecting {}:".format(self.edition.get_id())
        if rating:
            message = "{} rating {} ^".format(message, rating)
        message = "{} page {}".format(message, page_number)
        logger.info(message)
