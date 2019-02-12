# coding:utf-8
import json
from collections import OrderedDict, defaultdict
from collections.abc import Mapping
from copy import copy
from itertools import groupby

from typing import Optional, Tuple, Any

from lxml.etree import _Element

from stractor.trie_tree import TrieTree, TrieTreeNode
from stractor.wrappers import DomWrapper, ResultWrapper
from stractor.metas import ResultMeta


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
    def __init__(self, is_debug=False):
        self.trie_tree = TrieTree()
        self.debug_trie_tree = TrieTree()
        self.is_debug = is_debug

    def add_item(self, result_wrapper: ResultWrapper):
        self.trie_tree.add_item(
            result_wrapper.call_path,
            result_wrapper)

    def add_debug_item(self, path: Tuple, value: Any):
        if self.is_debug:
            self.debug_trie_tree.add_item(path, value)

    def export_result(self):
        import json
        print(json.dumps(self.trie_tree.root, cls=TupleKeyToStrings))
        new_tree = self.create_shortcut_tree(self.trie_tree.root)
        print('===========')
        print(json.dumps(new_tree.root, cls=TupleKeyToStrings))
        print('>>>>>>>>>>>>>>')

        # return self.trie_tree.root
        return self._export_result(new_tree.root).node_val.data

    def _create_shortcut_tree(self, root: TrieTreeNode):
        new_node = TrieTreeNode()
        new_node.node_val = root.node_val

        for child_name, child in root.items():
            if child.is_passthrough_node:
                last_node = TrieTreeNode._get_shortcut_last_node(child)
                name, value = next(iter(last_node.items()))
            else:
                name, value = child_name, child

            # Make sure that the order is kept
            name = (child_name[0], name[1])

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
        new_tree = TrieTree()
        new_tree.root = self._create_shortcut_tree(root)
        return new_tree

    @classmethod
    def _export_result(cls, root: TrieTreeNode):

        def get_idx_key(x): return x[0][0]

        data_children = []
        for child_name, child in root.items():
            child_ret = cls._export_result(child)
            data_children.append((child_name, child_ret))

        if not data_children:
            # Don't have any child, reached leaf, return
            return root

        data_children.sort()

        final_result: defaultdict = defaultdict(list)
        meta_opt_force_list = True
        for idx_grp_key, idx_grp in groupby(data_children, key=get_idx_key):
            buf: defaultdict = defaultdict(OrderedDict)
            print('new buf', idx_grp_key)
            merged_members = []
            unmerged_members = []
            for idx_group_member_tuple in idx_grp:
                member_trie_key, group_member = idx_group_member_tuple
                if group_member.node_val.meta.has_merged_data:
                    merged_members.append(group_member)
                else:
                    unmerged_members.append(group_member)

                # force_list defaults to True, if any one set it to Flase, then
                # the value should be False
                meta_opt_force_list = (
                    meta_opt_force_list and
                    group_member.node_val.meta.force_list)

            for group_member in unmerged_members:
                # unmerged members should be processed first because merged
                # members may be child of them
                fields_group_name = (
                    group_member.node_val.meta.fields_group_name)
                if fields_group_name:
                    buf[group_member.node_val.meta.fields_group_name
                        ].update(group_member.node_val.data)
                else:
                    buf.update(group_member.node_val.data)

            for group_member in merged_members:
                for child_grp_name, child_grp in (
                        group_member.node_val.data.items()):
                    if child_grp_name in buf:
                        buf[child_grp_name][child_grp_name] = child_grp
                    else:
                        buf[child_grp_name] = child_grp

            for k, v in buf.items():
                final_result[k].append(v)

        if not meta_opt_force_list:
            for group_name, group in final_result.items():
                if len(group) == 1:
                    final_result[group_name] = group[0]

        result = TrieTreeNode()
        result_meta = ResultMeta()
        result_meta.has_merged_data = True
        result.node_val = ResultWrapper(
            final_result, root.node_val.call_path, result_meta, False, False)
        print('This Level Result >>>>>>>>>>>>>>>>>>>>>>')
        print(json.dumps(final_result))
        return result

    def export_debug_result(self):

        print('======DEBUG=======')
        print(json.dumps(self._export_debug_result(
            self.debug_trie_tree.root), cls=TupleKeyToStrings))
        print('<<<<<<<<<<<<<<<<<')

    def _export_debug_result(self, root):

        data_result = []
        if root.has_val:
            if isinstance(root.node_val, DomWrapper):
                data_result.append(root.node_val.to_html())
            elif isinstance(root.node_val, ResultWrapper):
                data_result.append(root.node_val.data)
            else:
                print('root.data', type(root.node_val))

        child_results = {}
        for k, v in root.items():
            child_results[k] = self._export_debug_result(v)

        result = {
            'data': data_result,
            'children': child_results
        }
        return result
