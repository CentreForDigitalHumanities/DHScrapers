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
    review.edition_publisher = "edition_publisher"
    review.edition_publishing_year = "2020"
    review.date = "date"
    review.author = 'José'
    review.author_gender = 'mostly_female'
    review.language = 'language'
    review.rating = 'liked it'
    # review.rating_no added automatically
    review.text = 'text'

    expected = {
        'id': 'id',
        'url': 'url',
        'edition_id': 'edition_id',
        'edition_language': 'edition_language',
        'edition_publisher': 'edition_publisher',
        'edition_publishing_year' : '2020',
        'date': 'date',
        'author': 'José',
        'author_gender': 'mostly_female',
        'language': 'language',
        'rating': 'liked it',
        'rating_no': 3,
        'text': 'text'
    }

    assert review.to_dict() == expected
