# coding:utf-8

from typing import Iterable, Hashable, Any

from collections import defaultdict


class TrieTreeNode(defaultdict):
    def __init__(self):
        super().__init__(TrieTreeNode)
        self.data = None


class TrieTreeWithListData:

    def __init__(self):
        self.root = TrieTreeNode()

    def add_item(self,
                 prefixs: Iterable[Hashable],
                 value: Any):

        current_node = self.root
        for prefix in prefixs:
            current_node = current_node[prefix]
        if current_node.data is None:
            current_node.data = []
        current_node.data.append(value)
