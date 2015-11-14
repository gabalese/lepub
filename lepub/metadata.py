from lepub.utils import xpath, option


class Metadata(object):
    def __init__(self, opf_tree):
        self.__tree = xpath(opf_tree, './/opf:metadata')

    @property
    @option
    def title(self):
        return xpath(self.__tree, './/dc:title/text()')

    @property
    @option
    def author(self):
        return xpath(self.__tree, "//dc:creator[@opf:role='aut']/text()") or xpath(self.__tree, "//dc:creator/text()")

    @property
    @option
    def translator(self):
        return xpath(self.__tree, "//dc:creator[@opf:role='trl']/text()")


class Document(object):
    MIMETYPE = None

    def __init__(self, filename, content):
        self._filename = filename
        self._content = content

    @property
    def filename(self):
        return self._filename

    def content(self):
        return self._content.read()


class JSONAble(object):
    def json(self):
        pass
