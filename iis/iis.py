from iis.parsers import InputParser
from iis.collector import Collector

def scrape(inscriptions_xml_path, export_folder):
    with open(inscriptions_xml_path, 'r') as fin:
        input_parser = InputParser(fin.read())
        
    ids = input_parser.get_inscription_ids()
    Collector().collect(ids, export_folder)
