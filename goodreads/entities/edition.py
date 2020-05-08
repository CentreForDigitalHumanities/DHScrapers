from base_scraper.entities.book_edition import BookEdition as BaseBookEdition

class Edition(BaseBookEdition):

    def get_id(self):
        '''
        Return the last bit of the edition url (i.e. after the last /). Typically this will be the goodreads id.
        Example: '22561799-het-diner'. Returns None if there is no url.
        '''
        if not self.url: return None
        index = self.url.rfind('/') + 1
        return self.url[index:]
