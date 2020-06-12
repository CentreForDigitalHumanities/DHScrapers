import os
import json
from .parsers import ZoteroParser

responses = [
    {
        'file': 'IIP-453.json',
        'expected': 'Said, S. (2006). Two New Greek Inscriptions With The Name YTWR From Umm Al-Jimal. Palestine Exploration Quarterly, 125–132.'
    },
    {
        'file': 'IIP-645.json',
        'expected': 'Dalman, G. H. (1914). Inschriften aus Palästina. Zeitschrift Des Deutschen Palästina-Vereins, 37, 135–145.'
    },
    {
        'file': 'IIP-614.json',
        'expected': 'Fritz, V., & Deines, R. (1999). Catalogue of the Jewish Ossuaries in the German Protestant Institute of Archaeology. Israel Exploration Journal, 49(3/4), 222–241.'
    },
    {
        'file': 'IIP-434.json',
        'expected': 'Frey, J. B. (1975). Corpus of Jewish Inscriptions: Jewish Inscriptions from the Third Century B.C. to the Seventh Century A.D. New York: Ktav Pub. House'
    }
]

def test_get_source():
    for response in responses:
        _json = json.loads(get_test_file(response['file']))
        html = _json[0]['bib']
        parser = ZoteroParser(html)
        assert parser.get_source() == response['expected']


def get_test_file(file):
    test_file = get_test_data_path(file)
    with open(test_file, 'r') as file:
        return file.read()


def get_test_data_path(file):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata', file)
