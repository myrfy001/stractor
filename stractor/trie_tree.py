# coding:utf-8

from typing import Iterable, Hashable, Any, Dict, Optional

from collections import defaultdict


class TireNodeNoValue:
    call_path = ()
    __slots__ = ()


class TrieTreeNode(defaultdict):

    __slots__ = ('node_val',)

    def __init__(self):
        super().__init__(TrieTreeNode)
        self.node_val = TireNodeNoValue

    def replace_with_another_node(self, another: 'TrieTreeNode'):
        self.clear()
        self.update(another)
        self.node_val = another.node_val

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
            child_node = next(iter(child_node.values()))
            if child_node.is_passthrough_node:
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
            if (not child.has_val) and len(child) == 1:
                child_can_be_shortcut_names.append(child_name)

        for child_to_be_shortcut_name in child_can_be_shortcut_names:
            child_to_be_shortcut = self[child_to_be_shortcut_name]
            last_node = self._get_shortcut_last_node(child_to_be_shortcut)
            name, value = next(iter(last_node.items()))
            del self[child_to_be_shortcut_name]
            self[name] = value

    @property
    def has_val(self):
        return (self.node_val is not TireNodeNoValue)

    @property
    def is_passthrough_node(self):
        return (not self.has_val and len(self) == 1)


class TrieTree:

    def __init__(self):
        self.root = TrieTreeNode()

    def add_item(self,
                 prefixs: Iterable[Hashable],
                 value: Any):

        current_node = self.root
        for prefix in prefixs:
            current_node = current_node[prefix]
        current_node.node_val = value
