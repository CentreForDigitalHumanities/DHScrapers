import os
import sys
import argparse
from utilities.logging import init_logger
from iis.iis import scrape 

def main(sys_args):
    init_logger()
    args = parse_arguments(sys_args)
    scrape(args.inscriptions_xml_path, args.export_folder)


def folder_path(folder_path):
    '''
    Helper function to validate user input.
    folder_path will be created if it doesn't exist
    '''
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def parse_arguments(sys_args):
    '''
    Parse the supplied arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Scrape inscriptions from the IIP API.')

    parser.add_argument(
        '--inscriptions_xml_path', '-in', dest='inscriptions_xml_path', required=True,
        help="""Required. Path of the inscription id xml file. Typically in the input folder of this module.""")

    parser.add_argument(
        '--export_folder', '-ef', dest='export_folder', type=folder_path, required=True,
        help='''Path to the folder where you want the exports to appear. Should be a path to a folder, not a file.''')

    return parser.parse_args()

if __name__ == "__main__":
    main(sys.argv)
