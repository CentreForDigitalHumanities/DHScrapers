from .collector import GoodReadsReviewCollector
from goodreads.entities.edition import Edition

def test_get_page_url():
    e = Edition()
    e.url = 'http://whatever/id' # Note how id is used in url
    col = GoodReadsReviewCollector(e)
    url = col.get_page_url(1)
    assert url == 'https://www.goodreads.com/book/reviews/id?edition_reviews=true&text_only=true&page=1'

    url = col.get_page_url(5, 5)
    assert url == 'https://www.goodreads.com/book/reviews/id?edition_reviews=true&rating=5&page=5'
