from .edition import Edition

def test_get_id():
    edition = Edition()
    assert edition.get_id() == None
    edition.url = 'https://goodreads.com/book/show/16073029-the-dinner'
    assert edition.get_id() == '16073029-the-dinner'
    