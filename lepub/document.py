import lxml.html
from cached_property import cached_property
from collections import Counter
from utils import xpath


class Document(object):
    def __init__(self, filename, content):
        self._filename = filename
        self._content = content

    @property
    def __tree(self):
        return lxml.html.fromstring(self._content.read())

    @property
    def __body(self):
        return xpath(self.__tree, './/xhtml:body')

    @property
    def filename(self):
        return self._filename

    @cached_property
    def title(self):
        return xpath(self.__tree, './/title/text()')

    def content(self):
        return self._content.read()

    @property
    def text(self):
        return self.__tree.text_content() or None

    @property
    def letter_count(self):
        return sum(Counter(self.text).values())

    @property
    def word_count(self):
        return sum(Counter(self.text.split()).values())

    def as_json(self):
        return {
            'filename': self.filename,
            'title': self.title,
            'letter_count': self.letter_count,
            'word_count': self.word_count
        }

    def __unicode__(self):
        return "<Document: %s - %s>" % (self.title, self.filename)

    def __repr__(self):
        return self.__unicode__()

