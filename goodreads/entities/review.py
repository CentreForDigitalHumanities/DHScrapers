from base_scraper.entities.book_review import BookReview


class Review(BookReview):
    def __init__(self, metadata):
        # The order of the fields below determines the order of the field in csv exports!
        self.id = None
        self.url = None
        self.edition_id = None
        self.edition_language = None
        self.edition_publisher = None
        self.edition_publishing_year = None
        self.date = None
        self.author = None
        self.author_gender = None
        self.language = None
        self.rating = None
        self.rating_no = None
        for key, value in metadata.items():
            self.__setattr__(key, value)
        self.text = None
        

    def to_dict(self):
        '''
        Get a dict representing the review.
        Ideal for writing to csv using a DictWriter.
        '''

        as_dict = super().to_dict()
        as_dict.update(
            {'rating_no': self.get_rating_as_number()}
        )
        return as_dict

    def get_rating_as_number(self):
        '''
        Translate a number between 1 and 5 to the GoodReads equivalent
        '''
        if self.rating == 'did not like it':
            return 1
        if self.rating == 'it was ok':
            return 2
        if self.rating == 'liked it':
            return 3
        if self.rating == 'really liked it':
            return 4
        if self.rating == 'it was amazing':
            return 5
