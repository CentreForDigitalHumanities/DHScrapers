from base_scraper.parser import Parser as BaseScraper

class Parser(BaseScraper):

    def get_inscription_ids(self):
        ids = []
        
        docs = self.soup.find_all('doc')
        for doc in docs:
            ids.append(self.remove_whitespace(doc.get_text()))

        return ids
