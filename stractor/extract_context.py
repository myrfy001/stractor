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
            if child.has_data:
                data_children.append((child_name, child))
                node_meta = child.node_meta
                for child_name, parent_name in (
                        node_meta.group_to_parent_group_name_map.items()):
                    t = new_group_to_parent_group_name_map.setdefault(
                        child_name, parent_name)
                    if t != parent_name:
                        raise Exception(
                            f"The fields_group_name '{child_name}' has "
                            f"different parent_fields_group_name '{t}' and "
                            f"'{parent_name}'")
            else:
                child_ret = cls._export_result(child)
                print('---[Node Meta]---',
                      child_ret.node_meta.group_to_parent_group_name_map)
                data_children.append((child_name, child_ret))

        data_children.sort()

        final_result = defaultdict(list)
        meta_opt_force_list = True
        for idx_grp_key, idx_grp in groupby(data_children, key=get_idx_key):
            buf = defaultdict(OrderedDict)
            print('new buf', idx_grp_key)
            for idx_group_member_tuple in idx_grp:
                member_trie_key, group_member = idx_group_member_tuple
                node_meta = group_member.node_meta
                if group_member.has_data:
                    # this is a leaf data node
                    group_name = node_meta.fields_group_name
                    print('Merging Data Node-------------------------')
                    print('into:', group_name, id(buf[group_name]))
                    print('new data:',  json.dumps(group_member.data))
                    print('before merge',  json.dumps(buf[group_name]))
                    buf[group_name].update(group_member.data)
                    print('after merge',  json.dumps(buf[group_name]))
                    # if anyone unset force_list, it will take effect
                    meta_opt_force_list = (
                        meta_opt_force_list and node_meta.force_list)

                else:
                    # this is a merged child node

                    print('Merging Child Node-------------------------')
                    print('into:', id(buf))
                    print('new data:',  json.dumps(group_member.data))

                    print('before merge',  json.dumps(buf))
                    c2p_name_map = node_meta.group_to_parent_group_name_map
                    print('c2p_name_map',  json.dumps(c2p_name_map))
                    print('child_grp_name',  json.dumps(child_grp_name))
                    print('child_grp',  json.dumps(child_grp))
                    for child_grp_name, child_grp in group_member.data:
                        buf[c2p_name_map[child_grp_name]].update(child_grp)
                    print('after merge', json.dumps(buf))
                    # for group_name, group_data in group_member.data.items():
                    #     print('EEEEEEEEEE')
                    #     print(group_name, group_data)
                    #     buf[group_name].updaÈe(group_data)

            for k, v in buf.items():
                final_result[k].append(v)

        # if not meta_opt_force_list:
        #     for group_name, group in grouped_results.items():
        #         if len(grouped_results) == 1:
        #             grouped_results[group_name] = group[0]

        result = TrieTreeNode()
        result.data = final_result
        result_meta = ResultMeta()
        result_meta.group_to_parent_group_name_map = (
            new_group_to_parent_group_name_map)
        result.set_node_meta(result_meta)
        print('This Level Result >>>>>>>>>>>>>>>>>>>>>>')
        print(json.dumps(final_result))
        return result
