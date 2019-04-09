# coding:utf-8
from typing import List, Tuple, Dict, Union, Callable, Optional
from . import DomAccessComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.utils.document_merge import ConflictAction, conflict_enum_map
from stractor.component_registry import component_registry
from stractor.wrappers import DomWrapper
from stractor.engine import ExtractEngine
from stractor.components.selectors import SelectorBase


class ComponentDomShaver(DomAccessComponentBase):

    @classmethod
    def create_from_config(cls, config: Dict, engine: ExtractEngine):
        children = config.pop('children', [])
        group_name = config.pop('group_name', None)
        merge_conflict = conflict_enum_map[
            config.pop('merge_conflict', 'recursive')]
        force_list = config.pop('force_list', True)
        selectors_instances = cls.create_selectors_from_config(
            config.pop('selectors', []))
        component = cls(engine, children, group_name, merge_conflict,
                        force_list, selectors=selectors_instances, **config)
        return component

    def __init__(self,
                 engine: ExtractEngine,
                 children: List[Union[str, 'DomAccessComponentBase']],
                 group_name: Optional[bool],
                 merge_conflict: ConflictAction,
                 force_list: bool,
                 selectors: List[SelectorBase],
                 action='del_tree'):
        super().__init__(engine, children)
        self.selectors = selectors
        self.action = action
        self.group_name = group_name
        self.merge_conflict = merge_conflict
        self.force_list = force_list

    def process(self, domwrp: DomWrapper)-> List[DomWrapper]:
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times

        # make a copy if input is shared because we will modify it
        if domwrp.is_shared:
            domwrp = domwrp.clone(is_shared=self.output_is_shared)

        if self.action == 'del_tree':
            self._remove_tree_or_tag(domwrp, drop_tree)
        elif self.action == 'keep':
            self._keep_tree(domwrp)
        elif self.action == 'del_tag':
            self._remove_tree_or_tag(domwrp, drop_tag)
        return [domwrp]

    def _remove_tree_or_tag(self, domwrp: DomWrapper, action: Callable):
        input_dom = domwrp.data
        selected = []
        for selector in self.selectors:
            selected.extend(selector.process(input_dom))
        for dom in selected:
            if dom.getparent() is None:
                continue
            action(dom)

    def _keep_tree(self, domwrp: DomWrapper):
        input_dom = domwrp.data
        nodes_on_path_to_root = set()
        for selector in self.selectors:
            sels = selector.process(input_dom)
            for sel in sels:
                while sel is not None:
                    nodes_on_path_to_root.add(sel)
                    sel = sel.getparent()

        need_delete = set()
        for node in nodes_on_path_to_root:
            for sibling in node.itersiblings():
                if sibling not in nodes_on_path_to_root:
                    need_delete.add(sibling)
        for node in need_delete:
            drop_tree(node)
