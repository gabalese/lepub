import functools

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


def option(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            return None
    return wrapper


def first(*items):
    for item in items:
        if item:
            return item
    else:
        return None


def every(*items):
    if len(items) == 1:
        return items[0]
    return items
