import os
import sys
import logging
import argparse
from utilities.logging import init_logger
from goodreads.edition_scraper import scraper as editions_scraper
from goodreads.review_scraper import scraper as review_scraper

logger = logging.getLogger()

EDITION_LANGUAGES = ['English', 'German', 'Dutch', 'French', 'Spanish']


def main(sys_args):
    init_logger()

    args = parse_arguments(sys_args)
    if args.edition_languages == 'all':
        edition_languages = EDITION_LANGUAGES
    else:
        edition_languages = args.edition_languages
        if not isinstance(args.edition_languages, list):
            edition_languages = [args.edition_languages]
       
    editions = editions_scraper.scrape(args.editions_url,args.export_folder, args.editions_export_csv_filename)
    review_scraper.scrape(editions, args.export_folder, args.reviews_export_csv_filename, args.export_xml, edition_languages)
    logger.info('Done')


def csv_filename(filename):
    '''
    Helper function to validate user input.
    csv_filename should have .csv as extension.
    '''
    if not filename.endswith('.csv'):
        raise argparse.ArgumentTypeError(
            'File \'{}\' should have .csv extension'.format(filename))    
    return filename


def folder_path(folder_path):
    '''
    Helper function to validate user input.
    folder_path will be created if it doesn't exist
    '''
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def editions_url(url):
    '''
    Helper function to validate user input.
    Url must contain 
    '''
    required_bit = '/work/editions/'
    if not required_bit in url:
        raise argparse.ArgumentTypeError(
            'editions_url should contain {}'.format(required_bit)
        )
    return url


def parse_arguments(sys_args):
    '''
    Parse the supplied arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Scrape reviews for a title based on its various editions')

    parser.add_argument(
        '--editions_url', '--url', '-eu', dest='editions_url', type=editions_url, required=True,
        help="""Required. The url of an editions page. May or may not include the page queryparam at the end.
               You can find the url by clicking 'All Editions' (under 'Other Editions') on a title's page.
               Example: 'https://www.goodreads.com/work/editions/6463092-het-diner'""")

    parser.add_argument(
        '--export_folder', '-ep', dest='export_folder', type=folder_path, required=True,
        help='''Path to the folder where you want the exports to appear. Should be a path to a folder, not a file.''')
    
    parser.add_argument(
        '--reviews_export_csv_filename', '-ref', dest='reviews_export_csv_filename', type=csv_filename, required=True,
        help='''Filename for the csv you want to the reviews exported to. Should be a .csv file''')

    parser.add_argument(
        '--editions_export_csv_filename', '-eef', dest='editions_export_csv_filename', type=csv_filename,
        required=False, help='''Optional. Filename for the csv you want the editions exported to.
                Should be a .csv file. Editions will not be exported to csv if you leave this empty''')

    parser.add_argument(
        '--export_xml', '-ex', dest='export_xml', action='store_true', default=False,
        help='''If this flag is provided (no value needed), the reviews are exported to XML (in addition to CSV)''')

    parser.add_argument(
        '--edition_languages', '-el', dest='edition_languages',
        choices=(EDITION_LANGUAGES.append('all')), default='all', nargs="+",
        help="Optional. Choose one or multiple from the choices. Example: '-el English German'. Defaults to 'all\'")

    parsedArgs = parser.parse_args()
    return parsedArgs


if __name__ == "__main__":
    main(sys.argv)
