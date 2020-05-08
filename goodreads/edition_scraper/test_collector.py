from .collector import GoodReadsCollector

def test_get_page_url():
    col = GoodReadsCollector('https://www.goodreads.com/work/editions/6463092-het-diner')
    expected = 'https://www.goodreads.com/work/editions/6463092-het-diner?per_page=100&page=23'
    assert col.get_page_url(23) == expected
