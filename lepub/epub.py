import zipfile

from metadata import Metadata


class EPUB(Metadata):
    def __init__(self, input_file_path):
        self._file = zipfile.ZipFile(input_file_path, 'r')
        super(EPUB, self).__init__()

    @property
    def title(self):
        return self._title
