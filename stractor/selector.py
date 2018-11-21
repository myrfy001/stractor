#coding:utf-8
import copy
from lxml import etree
from .queryitem import QueryItem


class SelectorV1:
    def __init__(self, selector):
        self.name = selector['name']
        self.include = [QueryItem(x) for x in selector.get('include', [])]
        self.remove = [QueryItem(x) for x in selector.get('remove', [])]
        self.value = [QueryItem(x) for x in selector.get('value', [])]
        self.children = selector.get('children')
        if self.children is not None:
            # 相比于V1的格式，V1.5的格式将value移到了children中，如果一个节点没有
            # children，即该节点为叶子节点，则这个节点就是value。 此处代码，将叶子
            # 节点找出来，重新构成value，即实现从v1.5向v1的变换
            tmp_selectors = [SelectorV1(x) for x in self.children]
            selector_has_children = [
                x for x in tmp_selectors if (x.children or x.value)
            ]
            selector_no_child = [
                x for x in tmp_selectors if not (x.children or x.value)
            ]
            self.children = selector_has_children

            value = [{
                'name': x.name,
                'type': x.include[0].type,
                'query': x.include[0].queries
            } for x in selector_no_child]
            self.value += [QueryItem(x) for x in value]

    def select(self, docs, **kwargs):
        selected = []

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
                        selected.append(query_result)
                        select_dedup.add(query_result)

        value = []
        if self.value:
            for doc in selected:
                item_result = {}
                if not isinstance(doc, str):
                    for value_query in self.value:
                        val_ret = value_query.query(doc, **kwargs)
                        item_result[value_query.name] = val_ret
                else:
                    for value_query in self.value:
                        item_result[value_query.name] = [doc]
                if item_result:
                    value.append(item_result)

        children_result = []
        if self.children:
            for child in self.children:
                children_result.append(child.select(selected))

        return {
            "name": self.name,
            "value": value,
            "selected": selected,
            "children": children_result
        }
