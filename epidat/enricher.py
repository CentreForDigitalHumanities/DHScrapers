import html
import logging
from base_scraper.parser import Parser as BaseParser

logger = logging.getLogger(__name__)

class TEIEnricher(BaseParser):

    def __init__(self, xml):
        super().__init__(xml, 'xml')

    def add_publication_details(self, pub_details):
        '''
        Add `pub_details` by inserting it into the enricher's soup at the same place they are in the FIJI corpus,
        i.e. ['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'msIdentifier', 'publication']
        '''
        new_element = self.soup.new_tag('publications')
        for detail in pub_details:
            pub = self.soup.new_tag('publication')
            pub.string = detail
            new_element.append(pub)
        
        msIdentifier = self.soup.find('msIdentifier')
        if msIdentifier:
            msIdentifier.append(new_element)
        else:
            url = self.soup.find('idno').get_text()
            logger.warning('Something went wrong when appending publications to \'{}\''.format(url))
        return self.soup
