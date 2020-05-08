from .collector import Collector

def test_get_base_url():
    col = Collector()
    url_no_qp = "https://www.goodreads.com/work/editions/6463092-het-diner"
    url_one_qp = "https://www.goodreads.com/work/editions/6463092-het-diner?expanded=false"
    url_multiple_qp = "https://www.goodreads.com/work/editions/6463092-het-diner?expanded=false&per-page=100&page=8"
    expected = "https://www.goodreads.com/work/editions/6463092-het-diner"
    assert col.get_base_url(url_no_qp) == expected
    assert col.get_base_url(url_one_qp) == expected
    assert col.get_base_url(url_multiple_qp) == expected

def test_get_number_of_pages():
    col = Collector()
    assert col.get_number_of_pages(137, 100) == 2
    assert col.get_number_of_pages(6, 100) == 1
    assert col.get_number_of_pages(543, 100) == 6
    assert col.get_number_of_pages(100, 100) == 1
    assert col.get_number_of_pages(101, 100) == 2
    assert col.get_number_of_pages(261, 30) == 9
    assert col.get_number_of_pages(30, 30) == 1
    assert col.get_number_of_pages(31, 30) == 2
    assert col.get_number_of_pages(160, 30) == 6
