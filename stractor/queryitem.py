# coding:utf-8

from .exceptions import QuerierNotSupported


class QueryItem:

    REGISTERED_QUERIER_CLASSES = {}

    @classmethod
    def register_querier(cls, name, clazz):
        cls.REGISTERED_QUERIER_CLASSES[name] = clazz

    def __init__(self, query_item):
        self.type = query_item.get('type', 'xpath')

        self.queries = query_item.get('query', None)
        if not self.queries:
            raise Exception("QueryItem's query can't be empty", query_item)

        self.name = query_item.get('name', '')

        self.querier_class = self.REGISTERED_QUERIER_CLASSES.get(self.type)
        if self.querier_class is None:
            raise QuerierNotSupported(self.type)

    def query(self, doc, **kwargs):
        return self.querier_class.query(self.queries, doc, **kwargs)
