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

    def replace_with_another_node(self, another: 'TrieTreeNode'):
        self.clear()
        self.update(another)
        self.data = another.data
        self.node_meta = another.node_meta

    def shortcut_child(self, child_key: Hashable):
        child = self[child_key]
        if len(child) != 1:
            raise Exception(
                'Only a child with a single grandchild can be shortcut')
        grandchild_key, grandchild = next(iter(child.items()))
        del self[child_key]
        self[grandchild_key] = grandchild

    @staticmethod
    def _get_shortcut_last_node(first_node: 'TrieTreeNode'):
        '''
        @param first_node: The first node that can be shortcut, if no other 
        child of first_node can be shortcut, first_node will be returned. 

        >>> a = TrieTreeNode()
        >>> b = TrieTreeNode()
        >>> c = TrieTreeNode()
        >>> d = TrieTreeNode()

        >>> ret = TrieTreeNode._get_shortcut_last_node(a)
        >>> assert ret is a

        >>> a['b'] = b; b['c'] = c; c['d'] = d
        >>> ret = TrieTreeNode._get_shortcut_last_node(a)
        >>> assert ret is c  
        '''
        last_node = first_node
        child_node = first_node
        while 1:
            if len(child_node) != 1:
                break

            shortcut_stop_name, child_node = next(
                iter(child_node.items()))
            if ((not child_node.has_data) and len(child_node) == 1):
                last_node = child_node
            else:
                break
        return last_node

    def shortcut_children(self):
        '''
        >>> a = TrieTreeNode()
        >>> b1 = TrieTreeNode()
        >>> b2 = TrieTreeNode()
        >>> c = TrieTreeNode()
        >>> d = TrieTreeNode()
        >>> e = TrieTreeNode()

        >>> a['b1'] = b1; a['b2'] = b2
        >>> b2['c'] = c; c['d'] = d; d['e'] = e

        >>> a.shortcut_children()

        >>> assert a['b1'] is b1
        >>> assert a['e'] is e
        >>> assert 'b2' not in a
        '''

        child_can_be_shortcut_names = []
        for child_name, child in self.items():
            if (not child.has_data) and len(child) == 1:
                child_can_be_shortcut_names.append(child_name)

        for child_to_be_shortcut_name in child_can_be_shortcut_names:
            child_to_be_shortcut = self[child_to_be_shortcut_name]
            last_node = self._get_shortcut_last_node(child_to_be_shortcut)
            name, value = next(iter(last_node.items()))
            del self[child_to_be_shortcut_name]
            self[name] = value

    @property
    def has_data(self):
        return (self.data is not TireNodeNoData)


class TrieTreeWithMetaData:

    def __init__(self):
        self.root = TrieTreeNode()

    def add_item(self,
                 prefixs: Iterable[Hashable],
                 value: Any,
                 node_meta: Optional[Dict]):

        current_node = self.root
        for prefix in prefixs:
            current_node = current_node[prefix]
            print('prefix', prefix)
        current_node.data = value
        current_node.set_node_meta(node_meta)
