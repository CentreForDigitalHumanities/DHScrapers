import requests
import logging
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)

class Collector:

    def collect_html(self, url, remove_newlines=True, response_encoding=None, ignore_failed_request=False):
        '''
        Do the actual request and return the response.
        Raises an RunTimeError if the response status is not 200.
        The response is logged to file before that.

        Parameters:
            url -- the url to make the request to.
            remove_newlines -- specify whether newline charachters ('\n') should be removed 
                from response before returning it. Defaults to True.
            response_encoding -- the encoding used to return the response as text. Per the docs 
            (https://requests.readthedocs.io/en/master/user/quickstart/#response-content), request
            tries to guess the encoding, but may be wrong. By providing a value here, you can overwrite
            this default behaviour.
        '''
        r = self.make_request(url, ignore_failed_request)
        if not r:
            return None
        if response_encoding:
            r.encoding = response_encoding
        if remove_newlines: return r.text.replace("\n", "")
        return r.text


    def collect_json(self, url, ignore_failed_request=False):
        '''
        Do the actual request and return the response, i.e. response.json().
        Raises an RunTimeError if the response status is not 200.
        The response is logged to file before that.

        Parameters:
            url -- the url to make the request to.
        '''
        r = self.make_request(url, ignore_failed_request)
        return r.json()


    def make_request(self, url, ignore_failed_request):
        r = requests.get(url)
        logger.debug('response status: {}'.format(r.status_code))

        if r.status_code != 200:
            logger.error(r.text)
            if ignore_failed_request:
                return None
            raise RuntimeError("Could not collect from url {}".format(url))
        return r
    

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
