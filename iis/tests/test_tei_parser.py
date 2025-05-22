import os
from iis.parsers import TEIParser


files = [
    {
        'name': 'akld0024.xml',
        'details': [
            {
                'zotero_id': 'IIP-475',
                'unit': 'page',
                'numbers': [53]
            },
            {
                'zotero_id': 'IIP-053',
                'unit': 'page',
                'numbers': [66, 67]
            }
        ]
    },
    {
        'name': 'erra0001.xml',
        'details': [
            {
                'zotero_id': 'IIP-614',
                'unit': 'insc',
                'numbers': [1]
            },
            {
                'zotero_id': 'IIP-645',
                'unit': 'page',
                'numbers': [135]
            },
            {
                'zotero_id': 'IIP-434',
                'unit': None,
                'numbers': [None]
            }
        ]
    }
]


def test_get_bibl_details():
    for file in files:
        xml = get_test_file(file['name'])
        parser = TEIParser(xml)
        actual = parser.get_bib_details()
        assert actual == file['details']


def get_test_file(file):
    test_file = get_test_data_path(file)
    with open(test_file, 'r') as file:
        return file.read()


def get_test_data_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata', file)
