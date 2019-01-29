# coding:utf-8
from collections import OrderedDict
from collections.abc import Mapping
from copy import copy

from typing import Optional

from stractor.utils.trie_tree import TrieTreeWithMetaData, TrieTreeNode


class ExtractContext:
    def __init__(self):
        self.trie_tree = TrieTreeWithMetaData()

    def add_item(self, path, value, value_meta):
        self.trie_tree.add_item(path, value, value_meta)

    def export_result(self):
        import json
        print(json.dumps(self.trie_tree.root))
        dummy_node = TrieTreeNode()
        dummy_node['dummy_head'] = self.trie_tree.root
        self._remove_trie_tree_pass_through_node(dummy_node)
        self.trie_tree.root
        return self.trie_tree.root
        # return self._export_result(self.trie_tree.root)

    def _remove_trie_tree_pass_through_node(self, node: TrieTreeNode):

        if node.has_data:
            return

        node.shortcut_children()

        for child in node.values():
            self._remove_trie_tree_pass_through_node(child)

    def _export_result(self, root: TrieTreeNode):

        children_results = []
        for child in root.values():
            child_ret = self._export_result(child)
            children_results.append(child_ret)

        # if this level has no data, then pass through
        if not root.has_data:
            if len(children_results) == 1:
                return children_results[0]
            else:
                return children_results

        value, node_meta = root.data, root.node_meta
        fields_group_name = node_meta['fields_group_name']

        if len(value) == 1:
            if not node_meta['force_list']:
                value = value[0]

        if fields_group_name is not None:
            result = {fields_group_name: value}
        else:
            if isinstance(value, Mapping):
                # We don't know the class of the mapping,
                # maybe it's a dict, or ordered dict, so we copy it
                result = value.copy()
            elif isinstance(value, list):
                print('--------------------------')
                print(value)
                result = copy(value[0])
                if not isinstance(result, Mapping):
                    raise Exception('Should Be Mapping')
            else:
                raise Exception('Unknown Data Format')
        print('====', result)
        if children_results:
            result[node_meta['children_field_name']] = children_results
        return result
