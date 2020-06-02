import logging
from base_scraper.collector import Collector as BaseCollector 
from goodreads.entities.edition import Edition
from .parser import EditionPageParser

logger = logging.getLogger(__name__)

def collect(url):
    '''
    Collect all edition details from the given url.
    Returns a list of Edition instances.
    '''
    collector = GoodReadsCollector(url)

    # collect first page and see what we have
    page1_parser = collector.get_page_parser(1)
    number_of_editions = page1_parser.get_number_of_editions()
    number_of_pages = collector.get_number_of_pages(number_of_editions, 100)   
    editions = page1_parser.get_editions()

    if number_of_pages > 1:
        for page_number in range(2, number_of_pages + 1):
            parser = collector.get_page_parser(page_number) 
            editions.extend(parser.get_editions())

    return editions

class GoodReadsCollector(BaseCollector):
    def __init__(self, url):
        self.base_url = self.get_base_url(url)

    def get_page_parser(self, page_number):
        '''
        Get an instance of EditionPageParser with the requested page loaded.
        '''
        page_url = self.get_page_url(page_number)    
        logger.info("Collecting edition details from page {}".format(page_number))
        html = self.collect_html(page_url)
        return EditionPageParser(html)

    def get_page_url(self, page_number):
        '''
        Extend page url with queryparams specifying the page number
        and the number of results per page (i.e. 100)
        '''
        return "{}?per_page=100&page={}".format(self.base_url, page_number)
