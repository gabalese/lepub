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
