from lepub.utils import xpath


class OPF(object):
    def __init__(self, opf_tree):
        self.metadata = Metadata(opf_tree)


class Metadata(object):
    def __init__(self, opf_tree):
        self.__tree = xpath(opf_tree, './/opf:metadata')

    @property
    def title(self):
        return xpath(self.__tree, './/dc:title').text

    @property
    def author(self):
        return xpath(self.__tree, '//dc:creator').text
