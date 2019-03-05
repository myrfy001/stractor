# coding:utf-8
from typing import List, Tuple, Dict, Union, Callable, Optional
from . import DomAccessComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.utils.document_merge import ConflictAction, conflict_enum_map
from stractor.wrappers import DomWrapper
from stractor.component_registry import component_registry
from stractor.engine import ExtractEngine
from stractor.components.selectors import SelectorBase


class ComponentDomSelector(DomAccessComponentBase):

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
                 selectors: List[SelectorBase]):
        super().__init__(engine, children)
        self.selectors = selectors
        self.group_name = group_name
        self.merge_conflict = merge_conflict
        self.force_list = force_list

    def process(self, domwrp: DomWrapper)-> List[DomWrapper]:
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        input_dom = domwrp.data
        result = []
        for selector in self.selectors:
            sels = selector.process(input_dom)
            for sel in sels:
                result.append(
                    DomWrapper(
                        sel, self.output_is_shared, clone=True))
        return result
