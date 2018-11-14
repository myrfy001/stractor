# coding:utf-8

from lxml import etree

from html5_parser import parse

import parsel
import pprint
from .exceptions import VersionNotSupport, DocumentTypeNotSupportedForQuerier
from .selector import SelectorV1
from .transformer import Transformer

NoneType = type(None)


def object_to_dom(name, obj):

    if isinstance(obj, dict):
        node = etree.Element('dict')
        node.set('name', name)
        for k, v in obj.items():
            node.append(object_to_dom(k, v))
    elif isinstance(obj, list):
        node = etree.Element('list')
        node.set('name', name)
        for item in obj:
            node.append(object_to_dom(name, item))
    elif isinstance(obj, (int, float, bool, str, NoneType)):
        node = etree.Element('value')
        node.text = str(obj)
        node.set('name', name)
        node.set('type', type(obj).__name__)
    else:
        raise Exception('Not Supported Json Type')

    return node


class Extractor:
    @classmethod
    def create_doc(cls, data, **kwargs):
        if isinstance(data, str):
            doc = parse(data)
        elif isinstance(data, (dict, list)):
            doc = object_to_dom("root", data)
        elif not isinstance(data, parsel.Selector):
            raise DocumentTypeNotSupportedForQuerier()
        return doc

    def __init__(self, rule):
        self.version = rule['version']
        if self.version == '1':
            self.selector = SelectorV1(rule['selector'])
        else:
            raise VersionNotSupport()

        self.transformer = Transformer(rule.get('transformer', {}))

    def extract(self, docs, **kwargs):
        # import pprint as pp
        # pp = pprint.PrettyPrinter(indent=2)

        if not isinstance(docs, list):
            docs = [docs]
        ret = self.selector.select(docs, **kwargs)
        # pp.pprint(ret)
        ret = self.transformer.transform(ret, **kwargs)
        # pp.pprint(ret)

        return ret
