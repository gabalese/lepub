from lepub.utils import xpath
from jsonable import JSONAble


class TOC(JSONAble):
    def __init__(self, toc_tree):
        self.__tree = xpath(toc_tree, './/ncx:navMap')
        self.__items = [
            TOCItem(item) for item in self.__tree.getchildren()
        ]

    @property
    def items(self):
        return self.__items

    def __iter__(self):
        return iter(self.__items)

    def json(self):
        return super(TOC, self).json()


class TOCItem(object):
    def __init__(self, item):
        self.__item = item
        self.order = int(self.__item.get('playOrder'))
        self.label = xpath(self.__item, './/ncx:navLabel/ncx:text/text()')
        self.src = xpath(self.__item, './/ncx:content/@src')

    def as_json(self):
        return {
            'order': self.order,
            'label': self.label,
            'src': self.src
        }

