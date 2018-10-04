# coding:utf-8

import parsel

from ..exceptions import DocumentTypeNotSupportedForQuerier

parsel.selector._ctgroup


class DomQuerierBase:
    @classmethod
    def ensure_doc_type(cls, doc, **kwargs):
        # TODO
        pass


class XpathQuerier(DomQuerierBase):
    @classmethod
    def query(cls, queries, doc, **kwargs):
        parsel_selector = parsel.Selector(root=doc)
        result = []
        for query in queries:
            print('===', query)
            rets = parsel_selector.xpath(query)
            for ret in rets:
                result.append(ret.root)
        return result


class CssQuerier(DomQuerierBase):
    @classmethod
    def query(cls, queries, doc, **kwargs):
        parsel_selector = parsel.Selector(root=doc)
        result = []
        for query in queries:
            print('===', query)
            rets = parsel_selector.css(query)
            for ret in rets:
                result.append(ret.root)
        return result