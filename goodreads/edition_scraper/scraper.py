import logging
from .collector import collect as collect_editions
from base_scraper.exporter import EntityExporter

logger = logging.getLogger()

def scrape(url, export_folder, export_filename):
    '''
    Scrape the details of all editions of a title. 

    Parameters:
        url -- The url of an editions page. May or may not include the page queryparam at the end.
               You can find the url by clicking 'All Editions' (under 'Other Editions') on a title's page.
        export_folder -- Optional. The folder to create the export file in. If not None, export_filename must be supplied too.
        export_filename -- Optional. The name of the file to export to, must be a .csv file. If not None export_folder must be supplied to. 
    '''
    if export_filename and not export_folder:
        raise ValueError('if export_filename is set, so should export_folder')
    if export_filename and not export_filename.lower().endswith('.csv'):
        raise ValueError('export_filename must be a \'.csv\' file')

    editions = collect_editions(url)
    logger.info("{} editions collected from '{}'".format(len(editions), url))

    if export_filename:
        exporter = EntityExporter(export_folder, editions, 'editions', False)
        exporter.to_csv(export_filename)

    return editions
