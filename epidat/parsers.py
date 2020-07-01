from bs4 import NavigableString
from base_scraper.parser import Parser as BaseParser
from .constants import BASE_URL

class HowToHarvestParser(BaseParser):

    def get_record_list_urls(self):
        urls = []
        anchors = self.soup.find_all('a', text='list of records ')
        for a in anchors:
            urls.append("{}{}".format(BASE_URL, a['href']))
        return urls

class RecordListParser(BaseParser):

    def get_record_details(self):
        details = []
        resources = self.soup.find_all('resource')
        for r in resources:
            details.append({ 'id': r['id'], 'url': r['href'] })
        return details

class RecordHTMLParser(BaseParser):
    '''
    Parser the HTML version of a record (i.e. not the XML but the human friendly / web version).
    '''

    def get_publication_details(self):
        pubs = []
        quellen = self.soup.find('div', { 'id': 'q' })
        
        if quellen:
            p = quellen.find('p')
            for elem in p.contents:
                if type(elem) is NavigableString:
                    text = self.remove_whitespace(elem)
                    if text:
                        pubs.append(text)
        return pubs
