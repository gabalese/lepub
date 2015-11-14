from lxml import etree

from exceptions import InvalidEpub
from namespaces import NSMAP


class Metadata(object):
    def __init__(self):
        self._opf_path = self.get_opf_path()
        self._opf_tree = self.get_opf_tree(self._opf_path)
        self._title = self.get_title()

    def get_opf_path(self):
        with self._file.open('META-INF/container.xml') as container_file:
            container_root = etree.fromstring(container_file.read())
        rootfile = self.__xpath(container_root, './/container:rootfile')
        opf_path = rootfile.get('full-path')
        return opf_path

    def get_opf_tree(self, opf_path):
        with self._file.open(self._opf_path) as opf_file:
            self._opf_tree = etree.fromstring(opf_file.read())
        return self._opf_tree

    def get_title(self):
        return self.__xpath(self._opf_tree, './/dc:title').text

    @staticmethod
    def __xpath(tree, expression, namespaces=NSMAP):
        return XPathResults(tree.xpath(expression, namespaces=namespaces)).get()


class XPathResults(object):
    def __init__(self, results):
        self.__results = results

    def get(self):
        if len(self.__results) == 0:
            return None
        if len(self.__results) == 1:
            return self.__results[0]
        return self.__results
