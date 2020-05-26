from .base_entity import BaseEntity

class BookReview(BaseEntity):

    def __init__(self):
        self.id = None
        self.url = None
        self.edition_id = None
        self.edition_language = None
        self.date = None
        self.author = None
        self.author_gender = None
        self.language = None
        self.rating = None
        self.text = None

    def __str__(self):
        return self.id
