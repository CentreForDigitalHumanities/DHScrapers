from .review import Review


def test_to_dict():
    '''
    Test if adding an additional field works as expected.
    '''

    review = Review()
    review.id = 'id'
    review.url = "url"
    review.edition_id = "edition_id"
    review.edition_language = "edition_language"
    review.date = "date"
    review.author = ['author1', 'author2']
    review.language = 'language'
    review.rating = 'liked it'
    review.rating_no = 3
    review.text = 'text'

    expected = {
        'id': 'id',
        'url': 'url',
        'edition_id': 'edition_id',
        'edition_language': 'edition_language',
        'date': 'date',
        'author': ['author1', 'author2'],
        'language': 'language',
        'rating': 'liked it',
        'rating_no': 3,
        'text': 'text'
    }

    assert review.to_dict() == expected
