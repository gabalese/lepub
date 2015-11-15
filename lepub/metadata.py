from jsonable import JSONAble
from lepub.utils import xpath, first, every


class Metadata(JSONAble):
    def __init__(self, opf_tree):
        self.__unique_identifier_id = opf_tree.get('unique-identifier')
        self.__tree = xpath(opf_tree, './/opf:metadata')

    def __get_metadata_attribute(self, quantifier, *attributes):
        return quantifier(
            *[xpath(tree=self.__tree, expression=attribute, quantifier=quantifier)
              for attribute in attributes]
        )

    @property
    def identifier(self):
        if self.__unique_identifier_id:
            return self.__get_metadata_attribute(
                first,
                ".//dc:identifier[@id='%s']/text()" % self.__unique_identifier_id
            )
        else:
            return self.identifiers()[0]

    def identifiers(self):
        return self.__get_metadata_attribute(
            every,
            ".//dc:identifier/text()"
        )

    @property
    def title(self):
        return self.__get_metadata_attribute(
            first,
            './/dc:title/text()'
        )

    @property
    def description(self):
        return self.__get_metadata_attribute(
            first,
            './/dc:description/text()'
        )

    @property
    def language(self):
        return self.__get_metadata_attribute(
            every,
            './/dc:language/text()'
        )

    @property
    def rights(self):
        return self.__get_metadata_attribute(
            every,
            './/dc:rights/text()'
        )

    @property
    def publisher(self):
        return self.__get_metadata_attribute(
            first,
            './/dc:publisher/text()'
        )

    @property
    def author(self):
        return self.__get_metadata_attribute(
            first,
            ".//dc:creator[@opf:role='aut']/text()",
            "//dc:creator/text()"
        )

    @property
    def translator(self):
        return self.__get_metadata_attribute(
            first,
            ".//dc:creator[@opf:role='trl']/text()"
        )

    @property
    def date(self):
        return self.__get_metadata_attribute(
            first,
            ".//dc:date[@opf:event='ops-publication']/text()",
            ".//dc:date/text()"
        )

    @property
    def subject(self):
        return self.__get_metadata_attribute(
            every,
            ".//dc:subject/text()"
        )

    @property
    def publication_date(self):
        return self.__get_metadata_attribute(
            first,
            ".//dc:date[@opf:event='ops-publication']/text()",
        )
