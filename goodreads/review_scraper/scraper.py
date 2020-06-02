import sys
import logging
from .collector import collect
from base_scraper.exporter import EntityExporter

logger = logging.getLogger(__name__)


def scrape(editions, output_folder, csv_filename, export_xml=False, export_txt=False, edition_languages=['English', 'Dutch', 'German', 'Spanish', 'French']):
    '''
    Parameters:
        editions -- List of Edition instances to collect reviews for
        output_folder -- a full path to the folder where you expect the output. Subfolders (e.g. 'XML', 'CSV' will be created in this folder).
        csv_filename -- name (incl. extension) of the file to export reviews to in CSV format.
        export_xml -- Specify whether to export reviews as XML. Defaults to False.
        export_txt -- Specify whether to export reviews as TXT. Defaults to False.
        edition_languages -- specify the languages to include when collecting editions.
            Example: ['English', 'Dutch', 'German', 'Spanish', 'French']
            All other languages will be ignored. Defaults to ['English', 'Dutch', 'German', 'Spanish', 'French']
    '''
    reviews = []
    used_editions = 0
    editions_length = len(editions)

    for index, edition in enumerate(editions):
        if edition.language in edition_languages:
            logger.info("Collecting reviews for edition '{}' [{}/{}]".format(
                edition.get_id(), index + 1, editions_length))
            used_editions += 1
            reviews.extend(collect(edition))

    logger.info("{} reviews collected from {} editions".format(
        len(reviews), used_editions))

    exporter = EntityExporter(output_folder, reviews, 'reviews')
    exporter.to_csv(csv_filename)
    if export_xml:
        exporter.to_xml('review')
    if export_txt:
        exporter.to_txt()
