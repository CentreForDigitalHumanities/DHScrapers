import os
import logging
from base_scraper.parser import Parser
from base_scraper.collector import Collector as BaseCollector
from iis.constants import IIS_BASE_URL

logger = logging.getLogger(__name__)

class Collector(BaseCollector):

    def collect(self, inscription_ids, export_folder):
        '''
        Collect full EpiDoc documents for each inscription for which an id is supplied.
        Each inscription is immediately exported to file.
        '''
        number_of_inscriptions = len(inscription_ids)
        logger.info("Collecting {} inscriptions".format(number_of_inscriptions))

        for index, inscription_id in enumerate(inscription_ids):
            url = self.get_inscription_url(inscription_id)
            logger.info("Collecting from '{}' [{}/{}]".format(url, index + 1, number_of_inscriptions))
            xml = self.collect_html(url, remove_newlines=False, response_encoding='utf-8')
            
            # some extra actions to remove annoying whitespace in text nodes
            # parser = Parser(" ".join(xml.split()))
            # prettified_xml = parser.soup.prettify()

            self.export(export_folder, inscription_id, xml)

    
    def get_inscription_url(self, inscription_id):
        '''
        Helper method to put together an url for an inscription.
        '''
        return '{}{}'.format(IIS_BASE_URL, inscription_id)
    

    def export(self, export_folder, inscription_id, xml):
        '''
        Helper method to export inscription xml to an .xml file,
        in `export_folder` and with `inscription_id(.xml)` as name
        '''
        filename = os.path.join(export_folder, "{}{}".format(inscription_id, '.xml'))
        with open(filename, 'w', encoding='utf-8', newline='\n') as out_file:
            out_file.write(xml)
            logger.info("Exported inscription to '{}'".format(filename))
