from lepub.namespaces import NSMAP


def first(*items):
    for item in items:
        if item is not None:
            return item
    else:
        return None


def every(*items):
    if not items:
        return None
    if len(items) == 1:
        return items[0]
    return items


class XPathResults(object):
    def __init__(self, results):
        self.__results = results

    def get(self, quantifier):
        return quantifier(*self.__results)


def xpath(tree, expression, namespaces=NSMAP, quantifier=first):
    return XPathResults(tree.xpath(expression, namespaces=namespaces)).get(quantifier)
