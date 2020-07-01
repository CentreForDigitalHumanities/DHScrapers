import os
from .parsers import RecordHTMLParser

def test_get_publication_details():
    html = get_test_file('gda-33_html.html')
    actual = RecordHTMLParser(html).get_publication_details()
    assert actual == [
        'Standesamt Poppelsdorf, Sterbeurkunde 133/1854.',
        'Dan Bondy, Die jüdischen Grabsteine am Fuße des Godesberges, Dokumentation der Inschriften, in: Godesberger Heimatblätter 29, 1991, S. 5-39, hier S. 38.',
        'Klaus H. S. Schulte, Bonner Juden und ihre Nachkommen bis um 1930. Bonn 1976, S. 455, AAA und 456, Anm.3.'
    ]


def get_test_file(file):
    test_file = get_test_data_path(file)
    with open(test_file, 'r') as file:
        return file.read()


def get_test_data_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata', file)