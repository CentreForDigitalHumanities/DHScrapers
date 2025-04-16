import fileinput
import logging
import os
import sys

from bs4 import BeautifulSoup

from base_scraper.collector import Collector as BaseCollector
from iis.constants import ZOTERO_BASE_URL
from .parsers import TEIParser, ZoteroParser
from .enricher import TEIEnricher

logger = logging.getLogger(__name__)

class Collector(BaseCollector):

    def collect(self, import_folder: str, export_folder: str):
        '''
        Collect all Epidoc xml files which have changed since last harvest
        Enrich them with bibliographic data from Zotero and export to output folder
        '''
        change_file = os.path.join('iis', 'harvest-metadata', 'harvested-files.txt')
        with open(change_file) as f:
            num_records = sum(1 for _ in f)
        for _index in range(num_records):
            line = self.get_document_and_save_progress(change_file)
            filename = line.split("  ")[1].rstrip()
            logging.info(f"Processing file {filename}")
            inscription_id = os.path.splitext(filename)[0]
            with open(os.path.join(import_folder, filename), 'r') as xml_file:
                xml = xml_file.read()
                xml = self.enrich(inscription_id, xml)
                self.export(
                    os.path.join(export_folder, filename),
                    xml,
                )

    def get_document_and_save_progress(self, change_file: str) -> str:
        """Get the first document from the harvest file and remove it from the harvest file"""
        with fileinput.input(files=(change_file), inplace=True) as changed:
            for index, line in enumerate(changed):
                if index == 0:
                    output = line
                else:
                    sys.stdout.write(line)  # `print` would introduce newlines
            return output

    def enrich(self, inscription_id: str, xml: BeautifulSoup):
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

    def export(self, filename: os.PathLike, xml: BeautifulSoup):
        '''
        Helper method to export inscription xml to an .xml file,
        `filename` is expected to be the full path to the file.
        '''
        with open(filename, 'w', encoding='utf-8', newline='\n') as out_file:
            out_file.write(xml)
            logger.info("Exported inscription to '{}'".format(filename))
