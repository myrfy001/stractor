# coding:utf-8

import jsonpath_rw


class XpathQuerier:
    @classmethod
    def query(cls, queries, doc, base_url=None):
        result = []
        for query in queries:
            ret = doc.xpath(query)
            result.extend(ret)
        return result