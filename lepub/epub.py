import io
import os

from lepub.opf import OPFMixin
from lepub.document import Document


class EPUB(OPFMixin):
    def __init__(self, input_file_path):
        super(EPUB, self).__init__(input_file_path)
        self.metadata = self._opf.metadata
        self.manifest = self._opf.manifest
        self.spine = self._opf.spine
        self.guide = self._opf.guide
        self.toc = self.get_toc()

    def get(self, manifest_item):
        path_in_zip = os.path.join(os.path.dirname(self.get_opf_path()), manifest_item.href)
        document_data = self._file.read(path_in_zip)
        return Document(
            filename=os.path.basename(manifest_item.href),
            content=io.BytesIO(document_data)
        )
