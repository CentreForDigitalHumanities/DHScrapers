from bs4 import BeautifulSoup


class Parser():
    '''
    A base class for parsers.
    Gives you a BeautifulSoup instance in self.soup, with `html` parsed.
    Also, it offers a method to remove all whitespace characters from a string and
    add a space in between each word. For now, the rest is up to you.
    '''

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def remove_whitespace(self, text):
        '''
        Remove all whitespaces and join words with a space
        '''
        return " ".join(text.split())
