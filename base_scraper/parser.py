from bs4 import BeautifulSoup
import gender_guesser.detector as gender_detector


class Parser:
    '''
    A base class for parsers.
    Gives you a BeautifulSoup instance in self.soup, with `html` parsed.
    Gives you a GenderDetector in self.gender_detector (from the gender_guesser package).
    Also, it offers a method to remove all whitespace characters from a string and
    add a space in between each word. For now, the rest is up to you.
    '''

    def __init__(self, html, parser = 'html.parser'):
        self.soup = BeautifulSoup(html, parser)
        self.gender_detector = gender_detector.Detector()

    def remove_whitespace(self, text):
        '''
        Remove all whitespaces and join words with a space
        '''
        return " ".join(text.split())
