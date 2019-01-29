# coding:utf-8
import json
from collections import OrderedDict
from collections.abc import Mapping
from copy import copy
from itertools import groupby

from typing import Optional

from stractor.utils.trie_tree import TrieTreeWithMetaData, TrieTreeNode


class TupleKeyToStrings(json.JSONEncoder):
    def _encode(self, obj):
        if isinstance(obj, Mapping):
            t = {}
            for k, v in obj.items():
                v = self._encode(v)
                t[str(k)] = v
            return t
        else:
            return obj

    def encode(self, obj):
        return super(TupleKeyToStrings, self).encode(self._encode(obj))


class ExtractContext:
    def __init__(self):
        self.trie_tree = TrieTreeWithMetaData()

    def add_item(self, path, value, value_meta):
        self.trie_tree.add_item(path, value, value_meta)

    def export_result(self):
        import json
        print(json.dumps(self.trie_tree.root, cls=TupleKeyToStrings))
        new_tree = self.create_shortcut_tree(self.trie_tree.root)
        print('===========')
        print(json.dumps(new_tree.root, cls=TupleKeyToStrings))
        print('>>>>>>>>>>>>>>')
        # return self.trie_tree.root
        return self._export_result(new_tree.root).data

    def _create_shortcut_tree(self, root: TrieTreeNode):
        new_node = TrieTreeNode()
        new_node.data = root.data
        new_node.node_meta = root.node_meta

        for child_name, child in root.items():
            if child.is_passthrough_node:
                last_node = TrieTreeNode._get_shortcut_last_node(child)
                name, value = next(iter(last_node.items()))
            else:
                name, value = child_name, child

            # Make sure that the order is kept
            name = (name[0], child_name[1])

            value = self._create_shortcut_tree(value)
            new_node[name] = value

        return new_node

    def create_shortcut_tree(self, root: TrieTreeNode):

        # first step, get the first 'non-pass-through' node as the new root
        while 1:
            if root.is_passthrough_node:
                root = next(iter(root.values()))
            else:
                break
        # second step, process other parts of the tree
        new_tree = TrieTreeWithMetaData()
        new_tree.root = self._create_shortcut_tree(root)
        return new_tree

    def _export_result(self, root: TrieTreeNode):

        # used for group data at the same level
        def get_idx_from_key(x): return x[0][1]

        data_children = []
        for child_name, child in root.items():
            if child.has_data:
                data_children.append((child_name, child))
            else:
                child_ret = self._export_result(child)
                data_children.append((child_name, child_ret))

        data_children.sort(key=get_idx_from_key)

        merged_items = []
        for k, g in groupby(data_children, key=get_idx_from_key):
            buf = {}
            for group_member in g:
                buf.update(group_member[1].data)
            # print('///////////////')
            # print(buf)
            merged_items.append(buf)

        # node_meta = root.node_meta
        # if len(merged_items) == 1:
        #     if not node_meta['force_list']:
        #         merged_items = merged_items[0]

        result = {
            'children': merged_items
        }

        tmp = TrieTreeNode()
        tmp.data = result
        return tmp
