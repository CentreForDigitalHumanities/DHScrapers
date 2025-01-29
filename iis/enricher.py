from base_scraper.parser import Parser as BaseParser

class TEIEnricher(BaseParser):

    def __init__(self, xml):
        super().__init__(xml, 'xml')

    def add_source_details(self, bibl_details):
        '''
        Process `bibl_details` (including 'source'),
        and insert it into the enricher's soup at the same place they are in the FIJI corpus,
        i.e. ['teiHeader', 'fileDesc', 'sourceDesc', 'msDesc', 'msIdentifier', 'publication']
        '''
        sources = []
        for detail in bibl_details:
            source = detail['source']
            
            if 'unit' in detail and detail['unit']:
                numbers = None
                if detail['numbers'] and not (len(detail['numbers']) == 1 and not detail['numbers'][0]):
                    numbers = ", ".join(detail['numbers'])
                
                if not numbers:
                    source = '{} ({})'.format(source, detail['unit'])
                else:
                    source = '{} ({} {})'.format(source, detail['unit'], numbers)
            
            sources.append(source)

        new_element = self.soup.new_tag('publications')
        for source in sources:
            pub = self.soup.new_tag('publication')
            pub.string = source
            new_element.append(pub)
        self.soup.find('msIdentifier').append(new_element)
        return self.soup
