# coding:utf-8

from typing import Iterable, Hashable, Any, Dict, Optional

from collections import defaultdict


class TireNodeNoData:
    pass


class TrieTreeNode(defaultdict):

    __slot__ = ('has_data')

    def __init__(self):
        super().__init__(TrieTreeNode)
        self.data = TireNodeNoData
        self.node_meta = None

    def set_node_meta(self, value: Dict):
        # Node Meta can only be set once
        self.node_meta = self.node_meta or value

    @property
    def has_data(self):
        return (self.data is not TireNodeNoData)


class TrieTreeWithListData:

    def __init__(self):
        self.root = TrieTreeNode()

    def add_item(self,
                 prefixs: Iterable[Hashable],
                 value: Any,
                 node_meta: Optional[Dict]):

        current_node = self.root
        for prefix in prefixs:
            current_node = current_node[prefix]
        if current_node.data is TireNodeNoData:
            current_node.data = []
        current_node.data.append(value)
        if node_meta is not None:
            current_node.set_node_meta(node_meta)
