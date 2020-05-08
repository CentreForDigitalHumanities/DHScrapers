import requests
import logging
from urllib.parse import urlparse, urljoin

logger = logging.getLogger()

class Collector():

    def collect_html(self, url, remove_newlines=True):
        '''
        Do the actual request and return the response.
        Raises an RunTimeError if the response status is not 200.
        The response is logged to file before that.

        Parameters:
            url -- the url to make the request to.
            remove_newlines -- specify whether newline charachters ('\n') should be removed 
                from response before returning it. Defaults to True.
        '''
        r = requests.get(url)
        logger.debug('response status: {}'.format(r.status_code))

        if r.status_code != 200:
            logger.error(r.text)
            raise RuntimeError("Could not collect from url {}".format(url))
        
        if remove_newlines: return r.text.replace("\n", "")
        return r.text


    def get_base_url(self, url):
        '''
        Parse whatever url the user has provided to something without queryparameters
        '''
        parsed_url = urlparse(url)
        return urljoin(url, parsed_url.path)

    
    def get_number_of_pages(self, total_items, items_per_page):
        '''
        Given a certain number of items per page,
        establish the number of pages we need to collect.

        Neat trick to get rounded integers from https://stackoverflow.com/a/23590097.
        '''
        return int(total_items / items_per_page) + (total_items % items_per_page > 0)
