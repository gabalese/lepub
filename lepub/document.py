from bs4 import BeautifulSoup
from cached_property import cached_property
from collections import Counter


class Document(object):
    def __init__(self, filename, content):
        self._filename = filename
        self._content = content

    @cached_property
    def __soup(self):
        return BeautifulSoup(self._content, 'html.parser')

    @cached_property
    def __body(self):
        return self.__soup.find('body')

    @property
    def filename(self):
        return self._filename

    @cached_property
    def title(self):
        return self.__soup.title.text

    def content(self):
        return self._content.read()

    def text(self):
        return self.__body.text

    @cached_property
    def letter_count(self):
        return sum(Counter(self.text()).values())

    @cached_property
    def word_count(self):
        raise NotImplementedError()

    def as_json(self):
        return {
            'filename': self.filename,
            # 'title': self.title,
            'chars': self.letter_count()
        }

