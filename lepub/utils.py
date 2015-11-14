from lepub.namespaces import NSMAP


class XPathResults(object):
    def __init__(self, results):
        self.__results = results

    def get(self):
        if len(self.__results) == 0:
            return None
        if len(self.__results) == 1:
            return self.__results[0]
        return self.__results


def xpath(tree, expression, namespaces=NSMAP):
    return XPathResults(tree.xpath(expression, namespaces=namespaces)).get()
