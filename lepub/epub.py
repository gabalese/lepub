import zipfile

from lxml import etree

from lepub.utils import xpath
from metadata import OPF


class EPUB(object):
    def __init__(self, input_file_path):
        self._file = zipfile.ZipFile(input_file_path, 'r')
        self._opf = OPF(self.get_opf_tree(self.get_opf_path()))
        self.metadata = self._opf.metadata
        self.manifest = self._opf.manifest

    @property
    def title(self):
        return self.metadata.title

    @property
    def author(self):
        return self.metadata.author

    @property
    def translator(self):
        return self.metadata.translator

    def get_opf_path(self):
        with self._file.open('META-INF/container.xml') as container_file:
            container_root = etree.fromstring(container_file.read())
        rootfile = xpath(container_root, './/container:rootfile')
        opf_path = rootfile.get('full-path')
        return opf_path

    def get_opf_tree(self, opf_path):
        with self._file.open(opf_path) as opf_file:
            opf_tree = etree.fromstring(opf_file.read())
        return opf_tree
