from .base_entity import BaseEntity

class BookEdition(BaseEntity):
    '''
    Base class for an edition of a book.
    '''

    def __init__(self):        
        self.title = ''
        self.url = ''
        self.authors = []
        self.pub_details = ''
        self.edition_details = ''
        self.isbn = ''
        self.isbn13 = ''
        self.asin = ''
        self.language = ''
        self.avg_rating = None
        self.number_of_ratings = None    
    
    def __str__(self):
        return str(self.title)
    