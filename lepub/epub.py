import os
import zipfile
import io

from lxml import etree

from lepub.utils import xpath
from metadata import Document
from lepub.toc import TOC
from lepub.opf import OPF


class EPUB(object):
    def __init__(self, input_file_path):
        self._file = zipfile.ZipFile(input_file_path, 'r')
        self._opf = OPF(self.get_opf_tree(self.get_opf_path()))
        self.metadata = self._opf.metadata
        self.manifest = self._opf.manifest
        self.spine = self._opf.spine
        self.guide = self._opf.guide
        self.toc = self.get_toc()

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
        opf_path = xpath(container_root, './/container:rootfile/@full-path')
        return opf_path

    def get_opf_tree(self, opf_path):
        opf_tree = etree.fromstring(self._file.read(opf_path))
        return opf_tree

    def get_toc(self):
        return TOC(
            etree.fromstring(
                self.get(self.manifest.get('id', self._opf.spine.id)).content()
            )
        )

    def get(self, manifest_item):
        path_in_zip = os.path.join(os.path.dirname(self.get_opf_path()), manifest_item.href)
        document_data = self._file.read(path_in_zip)
        return Document(
            filename=os.path.basename(manifest_item.href),
            content=io.BytesIO(document_data)
        )
