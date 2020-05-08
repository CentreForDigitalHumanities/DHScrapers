import logging
from .collector import collect as collect_editions
from base_scraper.exporter import EntityExporter

logger = logging.getLogger()

def scrape(url, export_file):
    '''
    Scrape the details of all editions of a title. 

    Parameters:
        url -- The url of an editions page. May or may not include the page queryparam at the end.
               You can find the url by clicking 'All Editions' (under 'Other Editions') on a title's page.
        export_file -- Optional. The file to export the editions to, must be a .csv file. If not provided, no export is created.
    '''
    if export_file and not export_file.lower().endswith('.csv'):
        raise ValueError('export file must be a \'.csv\' file')

    editions = collect_editions(url)
    logger.info("{} editions collected from '{}'".format(len(editions), url))

    if export_file:
        exporter = EntityExporter(editions, 'editions', False)
        exporter.to_csv(export_file)

    return editions
