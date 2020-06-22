from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from iso639 import languages
from base_scraper.parser import Parser as BaseParser
from goodreads.entities.review import Review


class ReviewPageParser(BaseParser):
    def __init__(self, html, edition, min_review_length = 6):
        '''
        html - the html of one page of reviews
        edition - the edition these reviews belong to
        min_review_length - the minimum length of a single review (in characters). 
            Reviews shorter than this will be excluded. Defaults to 6.
        '''
        super().__init__(html)
        self.edition = edition
        self.reviews = self.soup.find_all('div', class_='review')
        self.min_review_length = min_review_length

    def contains_only_reviews(self):
        '''
        Establish if this is a page with only reviews or not.
        If it isn't, there are ratings in the review list.
        '''
        review_texts = self.get_reviews_texts()
        return len(review_texts) == len(self.reviews)

    def is_top_300(self):
        '''
        Establish if the current page is part of a Top 300.
        Ideal for checking if a text_only request returns all results,
        or if collecting per rating is necessary.
        '''
        count_elem = self.get_count_element()
        return 'top 300' in count_elem.text.lower()

    def get_number_of_text_only_reviews(self):
        '''
        Get the total number of text-only reviews for the edition (optionally limited to rating).
        This number is based on the 'Displaying X of Y' field. Therefore, if the current page
        is based on a rating, the number returned represent the total number of text-only reviews
        for the edition. Note that the current page contains only a subselection of this total.
        Returns 300 if current page is part of a top 300.
        '''
        if (self.is_top_300()):
            return 300
        count_elem = self.get_count_element()
        if not ' of ' in count_elem.text:
            return 0
        words = self.remove_whitespace(count_elem.text).strip().split(' ')
        return int(words[3])

    def get_count_element(self):
        '''
        Extract the element containg the 'Displaying X of Y reviews' text.
        '''
        return self.soup.find('div', class_='reviewSearchResults__count')

    def get_reviews_texts(self):
        '''
        Get only the reviews that contain text (i.e. ignore ratings)
        '''
        return self.soup.find_all('div', class_='reviewText')

    def get_reviews(self):
        '''
        Get Review instances parsed from the page's HTML.
        Ignores ratings (i.e. reviews without text)
        '''
        reviews = []
        for review_html in self.reviews:
            review_text_elem = review_html.find('div', class_='reviewText')
            if not review_text_elem:
                continue
            review_text = self.extract_review(review_text_elem)
            if len(review_text) < self.min_review_length:
                continue
            review = Review()
            review.id = review_html['id']
            review.url = review_html.find('link')['href']
            review.edition_language = self.edition.language
            review.edition_id = self.edition.get_id()
            review.edition_publisher = self.edition.publisher
            review.edition_publishing_year = self.edition.publishing_year
            review.author = self.get_text_or_none(
                review_html.find('a', class_='user'))
            review.author_gender = self.gender_detector.get_gender(
                review.author.split()[0])
            review.date = self.get_text_or_none(
                review_html.find('a', class_='reviewDate'))
            review.text = review_text
            review.rating = self.get_text_or_none(
                review_html.find('span', class_='staticStar'))
            review.language = self.get_review_language(review.text)            
            reviews.append(review)
        return reviews

    def get_review_language(self, review_text):
        language = 'UNKNOWN'
        
        # handle the rare case where there is a reviewText element but no actual text
        if not review_text:
            return language

        try:
            language_code = detect(review_text)
            if language_code.startswith('zh'):
                # there are two language codes for Chinese ('zh-cn' and 'zh-tw') in langdetecct,
                # both of which the iso639 module cannot deal with (it only knows zh)
                language_code = 'zh'

            iso639_language = languages.get(alpha2=language_code)
            if iso639_language:
                language = iso639_language.name
        except LangDetectException:
            # langdetect can't deal with texts that consist of only things like
            # '3.5-4/5', or '(...) 6/10'
            pass
            
        return language

    def extract_review(self, review_text_elem):
        container = review_text_elem.find('span', class_='readable')
        spans = container.find_all('span')
        # always extract the text from the last <span>.
        # There are rare cases when there is a <div> with 'reviewText' class in the HTML,
        # without there actually being any text in the field. Ignore those.
        if spans:
            return self.get_text_or_none(spans[-1])
        else:
            return None

    def get_text_or_none(self, field):
        if field:
            return self.remove_whitespace(field.get_text(' '))
        return None
