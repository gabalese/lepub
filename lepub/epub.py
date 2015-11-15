import io
import os

from lepub.opf import OPFMixin
from lepub.document import Document
from jsonable import JSONAble


class EPUB(OPFMixin, JSONAble):
    def __init__(self, input_file_path):
        super(EPUB, self).__init__(input_file_path)
        self.metadata = self._opf.metadata
        self.manifest = self._opf.manifest
        self.spine = self._opf.spine
        self.guide = self._opf.guide
        self.toc = self.get_toc()

    @property
    def documents(self):
        return [
            self.open(item.src) for item in self.toc
        ]

    def get(self, manifest_item):
        path_in_zip = os.path.join(os.path.dirname(self.get_opf_path()), manifest_item.href)
        document_data = self._file.read(path_in_zip)
        return Document(
            filename=os.path.basename(manifest_item.href),
            content=io.BytesIO(document_data)
        )

    def open(self, href):
        path_in_zip = os.path.join(os.path.dirname(self.get_opf_path()), href)
        document_data = self._file.read(path_in_zip)
        return Document(
            filename=os.path.basename(path_in_zip),
            content=io.BytesIO(document_data)
        )
