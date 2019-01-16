# coding:utf-8

from stractor.utils.trie_tree import TrieTreeWithListData


class ExtractContext:
    def __init__(self):
        self.trie_tree = TrieTreeWithListData()

    def add_item(self, path, value):
        self.trie_tree.add_item(path, value)

    def _export_result(self, root: TrieTreeWithListData):
        result = None
        if root.data is not None:

        for child in root:
            self._export_result(child)

        return result
