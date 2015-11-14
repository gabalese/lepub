from lepub.utils import xpath, option
from lxml.etree import Comment


class OPF(object):
    def __init__(self, opf_tree):
        self.metadata = Metadata(opf_tree)
        self.manifest = Manifest(opf_tree)


class Metadata(object):
    def __init__(self, opf_tree):
        self.__tree = xpath(opf_tree, './/opf:metadata')

    @property
    @option
    def title(self):
        return xpath(self.__tree, './/dc:title').text

    @property
    @option
    def author(self):
        try:
            return xpath(self.__tree, "//dc:creator[@opf:role='aut']").text
        except ValueError:
            return xpath(self.__tree, "//dc:creator").text

    @property
    @option
    def translator(self):
        return xpath(self.__tree, "//dc:creator[@opf:role='trl']").text


class Manifest(object):
    def __init__(self, opf_tree):
        self.__tree = xpath(opf_tree, './/opf:manifest')
        self.__items = [
            ManifestItem(item) for item in self.__tree.getchildren()
            if item.tag is not Comment
        ]

    @property
    def stylesheets(self):
        return self.filter('type', 'text/css')

    @property
    def documents(self):
        return self.filter('type', ['application/xhtml+xml'])

    @property
    def media(self):
        return self.filter('type', ['image/png', 'image/jpeg', 'image/gif'])

    def filter(self, key, values):
        if type(values) != list:
            values = [values]
        return filter(lambda el: getattr(el, key) in values, self.__items)

    def __len__(self):
        return len(self.__items)

    def __getitem__(self, item):
        return self.__items[item]


class ManifestItem(object):
    def __init__(self, item):
        self.id = item.get('id')
        self.href = item.get('href')
        self.type = item.get('media-type')
