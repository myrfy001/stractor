# coding:utf-8
import json
from collections import OrderedDict, defaultdict
from collections.abc import Mapping
from copy import copy
from itertools import groupby

from typing import Optional

from stractor.utils.trie_tree import TrieTreeWithMetaData, TrieTreeNode
from stractor.result_meta import ResultMeta


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
        new_tree = TrieTreeWithMetaData()
        new_tree.root = self._create_shortcut_tree(root)
        return new_tree

    @classmethod
    def _export_result(cls, root: TrieTreeNode):

        def get_idx_key(x): return x[0][0]

        new_group_to_parent_group_name_map = {}
        data_children = []
        for child_name, child in root.items():
            child_ret = cls._export_result(child)
            data_children.append((child_name, child_ret))
            node_meta = child_ret.node_meta

        if not data_children:
            # Don't have any child, reached leaf, return
            return root

        data_children.sort()

        final_result = defaultdict(list)
        meta_opt_force_list = True
        for idx_grp_key, idx_grp in groupby(data_children, key=get_idx_key):
            buf = defaultdict(OrderedDict)
            print('new buf', idx_grp_key)
            merged_members = []
            unmerged_members = []
            for idx_group_member_tuple in idx_grp:
                member_trie_key, group_member = idx_group_member_tuple
                if group_member.node_meta.has_merged_data:
                    merged_members.append(group_member)
                else:
                    unmerged_members.append(group_member)

            for group_member in unmerged_members:
                # unmerged members should be processed first because merged
                # members may be child of them
                c2p_name_map = (
                    group_member.node_meta.fields_to_parent_fields_name_map)
                for child_name, child_value in group_member.data.items():
                    buf[c2p_name_map[child_name]
                        ][child_name] = child_value

            for group_member in merged_members:
                for child_grp_name, child_grp in group_member.data.items():
                    if child_grp_name in buf:
                        buf[child_grp_name][child_grp_name] = child_grp
                    else:
                        buf[child_grp_name] = child_grp

            for k, v in buf.items():
                final_result[k].append(v)

        # if not meta_opt_force_list:
        #     for group_name, group in grouped_results.items():
        #         if len(grouped_results) == 1:
        #             grouped_results[group_name] = group[0]

        result = TrieTreeNode()
        result.data = final_result
        result_meta = ResultMeta()
        result_meta.has_merged_data = True
        result.set_node_meta(result_meta)
        print('This Level Result >>>>>>>>>>>>>>>>>>>>>>')
        print(json.dumps(final_result))
        return result
