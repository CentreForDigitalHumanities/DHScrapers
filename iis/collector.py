import os
import logging
from base_scraper.collector import Collector as BaseCollector
from iis.constants import IIS_BASE_URL, ZOTERO_BASE_URL
from .parsers import TEIParser, ZoteroParser
from .enricher import TEIEnricher

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
            if os.path.isfile(os.path.join(export_folder, '{}.xml'.format(inscription_id))):
                continue
            xml = self.collect_html(url, remove_newlines=False, response_encoding='utf-8', ignore_failed_request=True)
            if not xml:
                continue
            
            xml = self.enrich(inscription_id, xml)

            self.export(export_folder, inscription_id, xml)


    def enrich(self, inscription_id, xml):
        '''
        Enrich the inscription XML with publication details (collected from Zotero) 
        and return it.
        '''
        bibl_details = TEIParser(xml).get_bib_details()
        for detail in bibl_details:
            _id = detail['zotero_id']
            url = ZOTERO_BASE_URL.format(_id)
            logger.info('   Enriching inscription {} with data from {}'.format(inscription_id, url))
            response = self.collect_json(url, ignore_failed_request=True)            
            if response and len(response) > 0:
                detail['source'] = ZoteroParser(response[0]['bib']).get_source()
            else:
                detail['source'] = ''
        
        return str(TEIEnricher(xml).add_source_details(bibl_details))

    
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
