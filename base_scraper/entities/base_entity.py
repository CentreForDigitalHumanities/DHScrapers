class BaseEntity:
    '''
    Base class for scrapable entities (e.g. book editions, book reviews, etc)

    Provide some basics that shuold be available on all such entities, such as `to_dict()`.
    '''

    def to_dict(self):
        '''
        Get the entity instance as a dict.
        '''
        return vars(self)