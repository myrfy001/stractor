# coding:utf-8
from html5_parser import parse

import parsel
import pprint
from .exceptions import VersionNotSupport, DocumentTypeNotSupportedForQuerier
from .selector import Selector


class Extractor:
    @classmethod
    def create_doc(cls, data, **kwargs):
        if isinstance(data, str):
            doc = parse(data)
        elif not isinstance(data, parsel.Selector):
            raise DocumentTypeNotSupportedForQuerier()
        return doc

    def __init__(self, rule):
        self.version = rule['version']
        if self.version != '1':
            raise VersionNotSupport()
        self.selector = Selector(rule['selector'])

    def extract(self, doc, **kwargs):
        ret = self.selector.select(doc, **kwargs)
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(ret)
