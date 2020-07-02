import os
import sys
import csv
import re
import argparse
import logging
from utilities.logging import init_logger
from goodreads.constants import EDITION_LANGUAGES
from goodreads.goodreads import scrape

logger = logging.getLogger(__name__)


def main(sys_args):
    init_logger()
    args = parse_arguments(sys_args)
    if args.edition_languages == 'all':
        edition_languages = EDITION_LANGUAGES
    else:
        edition_languages = args.edition_languages
        if not isinstance(args.edition_languages, list):
            edition_languages = [args.edition_languages]

    if args.title_file:
        title_infos = get_title_infos(args.title_file)
        
        # first validate the url input
        for title_info in title_infos:
            editions_url(title_info['editions_url'])

        for title_info in title_infos:
            logger.info('Starting scrape for {}'.format(title_info['title']))

            sub_folder_name = get_valid_filename(title_info['title'])
            export_folder = os.path.join(args.export_folder, sub_folder_name)
            if not os.path.exists(export_folder):
                os.makedirs(export_folder)
            scrape(
                title_info['editions_url'],
                export_folder,
                edition_languages,
                args.editions_csv_filename,
                args.reviews_csv_filename,
                args.export_xml,
                args.export_txt,
                args.min_review_length,
                title_info['metadata']
            )
    
    if args.editions_url:
        scrape(
            args.editions_url,
            args.export_folder,
            edition_languages,
            args.editions_csv_filename,
            args.reviews_csv_filename,
            args.export_xml,
            args.export_txt,
            args.min_review_length
        )


def get_title_infos(path):
    result = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f, delimiter=";")
        metadata_fieldnames = reader.fieldnames[2:]
        for row in reader:            
            metadata = {}
            for field in metadata_fieldnames:
                metadata[field] = row[field]
            result.append({
                'title': row['title'],
                'editions_url': row['editions_url'],
                'metadata': metadata
            })
    return result

def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    Stolen from https://github.com/django/django/blob/master/django/utils/text.py
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


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
    Url must contain '/work/editions/'
    '''
    required_bit = '/work/editions/'
    if not required_bit in url:
        raise argparse.ArgumentTypeError(
            'editions_url `{}` should contain {}'.format(url, required_bit)
        )
    return url


def parse_arguments(sys_args):
    '''
    Parse the supplied arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Scrape reviews for a title based on its various editions')

    _input_group = parser.add_mutually_exclusive_group(required=True)
    
    _input_group.add_argument(
        '--editions_url', '--url', '-eu', dest='editions_url', type=editions_url,
        help="""The url of an editions page. May or may not include the page queryparam at the end.
               You can find the url by clicking 'All Editions' (under 'Other Editions') on a title's page.
               Example: 'https://www.goodreads.com/work/editions/6463092-het-diner'""")

    _input_group.add_argument(
        '--title_file', dest='title_file', help="""Path to a csv file containing at least two columns: title, 
            editions_url. Any columns after that will be added as metadata to each review."""    )

    parser.add_argument(
        '--export_folder', '-ef', dest='export_folder', type=folder_path, required=True,
        help='''Path to the folder where you want the exports to appear. Should be a path to a folder, not a file.''')

    parser.add_argument(
        '--reviews_export_csv_filename', '-ref', dest='reviews_csv_filename', type=csv_filename, default='reviews.csv',
        help="Filename for the csv you want to the reviews exported to. Should be a .csv file. Defaults to 'reviews.csv'")

    parser.add_argument(
        '--editions_export_csv_filename', '-eef', dest='editions_csv_filename', type=csv_filename,
        required=False, help='''Optional. Filename for the csv you want the editions exported to.
                Should be a .csv file. Editions will not be exported to csv if you leave this empty''')

    parser.add_argument(
        '--export_xml', '--xml', dest='export_xml', action='store_true', default=False,
        help='''If this flag is provided (no value needed), the reviews are exported to XML (in addition to CSV)''')

    parser.add_argument(
        '--export_txt', '--txt', dest='export_txt', action='store_true', default=False,
        help='''If this flag is provided (no value needed), the reviews are exported to TXT (in addition to CSV)''')

    parser.add_argument(
        '--edition_languages', '-el', dest='edition_languages',
        choices=(EDITION_LANGUAGES.append('all')), default='all', nargs="+",
        help="Optional. Choose one or multiple from the choices. Example: '-el English German'. Defaults to 'all\'")

    parser.add_argument(
        '--min_review_length', '--min_length', '-mrl', dest='min_review_length', default=6, type=int,
        help="Optional. the minimum length of a single review (in characters). Reviews shorter than this will be excluded. Defaults to 6.")

    parsedArgs = parser.parse_args()
    return parsedArgs


if __name__ == "__main__":
    main(sys.argv)
