from bs4 import BeautifulSoup
import resid

from surflink import exception


class Document():
    '''Template for object created from HTML or XML markup'''
    def __init__(self, markup, url=None, attrs=("src", "href")) -> None:
        self._markup = markup
        self._attrs = attrs
        self._url = url
        self._url_provided = url != None
        if self._url_provided and resid.is_url(url):
            raise exception.URLError("'{}' is not url")
        # Creates beutufulsoup to parse provided markup
        self._soup = BeautifulSoup(markup, 'html.parser')

    def get_soup(self):
        return self._soup

