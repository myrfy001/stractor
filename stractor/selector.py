#coding:utf-8
import copy
from lxml import etree
from .queryitem import QueryItem


class Selector:
    def __init__(self, selector):
        self.name = selector['name']
        self.include = [QueryItem(x) for x in selector.get('include', [])]
        self.remove = [QueryItem(x) for x in selector.get('remove', [])]
        self.children = selector.get('children')
        if self.children is not None:
            self.children = [Selector(x) for x in self.children]

    def select(self, docs, **kwargs):
        results = []

        if self.remove:
            for doc in docs:
                for remove in self.remove:
                    rem_ret = remove.query(doc, **kwargs)
                    for query_result in rem_ret:
                        if not isinstance(query_result, etree._Element):
                            continue
                        query_result.getparent().remove(query_result)

        select_dedup = set()
        for doc in docs:
            for include in self.include:
                inc_ret = include.query(doc, **kwargs)
                for query_result in inc_ret:
                    if query_result not in select_dedup:
                        results.append(query_result)
                        select_dedup.add(query_result)
                print(results)

        children_result = []
        if self.children:
            for child in self.children:
                children_result.append(child.select(results))

        return {
            "name": self.name,
            "value": results,
            "children": children_result
        }
