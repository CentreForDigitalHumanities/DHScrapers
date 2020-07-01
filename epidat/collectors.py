import logging
from base_scraper.collector import Collector as BaseCollector
from .constants import HOW_TO_HARVEST_URL, BASE_URL
from .parsers import HowToHarvestParser, RecordListParser, RecordHTMLParser
from .enricher import TEIEnricher

logger = logging.getLogger(__name__)


class EpidatCollector(BaseCollector):

    def collect_record_list_urls(self):
        '''
        Collect the urls for the list of records belonging to each code (e.g. 'ad2').
        Simply returns a list of urls. 
        '''
        logger.info('Collecting starting point from {}'.format(
            HOW_TO_HARVEST_URL))
        html = self.collect_html(HOW_TO_HARVEST_URL)
        return HowToHarvestParser(html).get_record_list_urls()

    def collect_record_details(self, record_list_url):
        '''
        Collect the id and url for each record found in the list at `record_list_url`.
        Returns a list of dicts: { 'id': '<id>', 'url': <url>' }.
        '''        
        html = self.collect_html(record_list_url)
        return RecordListParser(html).get_record_details()

    def collect_record(self, record_detail):
        xml = self.collect_html(record_detail['url'])
        return str(self.enrich(xml, record_detail))

    def enrich(self, record_xml, record_detail):
        pub_details = self.collect_publication_details(record_detail)
        return TEIEnricher(record_xml).add_publication_details(pub_details)

    def collect_publication_details(self, record_detail):
        '''
        Extract publication details from the records' HTML page (i.e. the human friendly version).
        Returns a list of strings.
        '''
        url = '{}?id={}'.format(BASE_URL, record_detail['id'])
        logger.info('   Enriching {} with data from {}'.format(
            record_detail['id'], url))
        html = self.collect_html(url)
        return RecordHTMLParser(html).get_publication_details()
