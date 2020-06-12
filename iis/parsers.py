from base_scraper.parser import Parser as BaseParser


class InputParser(BaseParser):

    def get_inscription_ids(self):
        ids = []

        docs = self.soup.find_all('doc')
        for doc in docs:
            ids.append(self.remove_whitespace(doc.get_text()))

        return ids


class ZoteroParser(BaseParser):

    def get_source(self):
        return self.remove_whitespace(self.soup.text)


class TEIParser(BaseParser):

    def __init__(self, xml):
        super().__init__(xml, 'xml')

    def get_bib_details(self):
        '''
        Extract source details. Returns a list of objects like this:
        { 
            'zotero_id': 'Zotero id of the source', 
            'unit': 'page|insc'
            'numbers': 'array with all unit numbers encountered' 
        }
        '''
        details = []
        existing_ids = []
        bibls = self.soup.find_all('bibl')
        for bibl in bibls:            
            zotero_id = bibl.ptr['target'][:-4]
            if 'unit' in bibl.biblScope.attrs:
                unit = bibl.biblScope['unit']
            else: unit = None
            if bibl.biblScope.text:
                number = bibl.biblScope.text
            else: number = None

            if zotero_id in existing_ids:
                result = next((x for x in details if x['zotero_id'] == zotero_id))
                result['numbers'].append(number) 
                result['numbers'].sort()
            else:
                result = {
                    'zotero_id': zotero_id,
                    'unit': unit,
                    'numbers': [number]
                }
                details.append(result)
                existing_ids.append(zotero_id)

        return details
