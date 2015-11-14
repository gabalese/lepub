from lxml.etree import Comment

from lepub.exceptions import InvalidEpub
from lepub.metadata import Metadata
from lepub.utils import xpath


class OPF(object):
    def __init__(self, opf_tree):
        self.metadata = Metadata(opf_tree)
        self.manifest = Manifest(opf_tree)
        self.spine = Spine(opf_tree, self.manifest)
        self.guide = Guide(opf_tree)
        self.toc_id = self.spine.id


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

    def get(self, key, values):
        filtered = self.filter(key, values)
        if len(filtered) == 1:
            return filtered[0]
        if len(filtered) > 1:
            raise InvalidEpub("More than one element for idref")
        else:
            return None

    def __len__(self):
        return len(self.__items)

    def __getitem__(self, item):
        return self.__items[item]


class ManifestItem(object):
    def __init__(self, item):
        self.id = item.get('id')
        self.href = item.get('href')
        self.type = item.get('media-type')


class Spine(object):
    def __init__(self, opf_tree, manifest):
        self.__tree = xpath(opf_tree, './/opf:spine')
        self.__manifest = manifest

    @property
    def id(self):
        return self.__tree.get('toc')

    @property
    def items(self):
        return [
            self.__manifest.get('id', spine_item.get('idref'))
            for spine_item in self.__tree
        ]


class Guide(object):
    def __init__(self, opf_tree):
        self.__tree = xpath(opf_tree, './/opf:guide')
        self.__items = [
            Reference(item) for item in self.__tree
        ]

    @property
    def items(self):
        return self.__items


class Reference(object):
    def __init__(self, item):
        self.type = item.get('type')
        self.title = item.get('title')
        self.href = item.get('href')
