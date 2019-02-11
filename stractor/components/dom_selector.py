# coding:utf-8
from typing import List, Tuple, Dict, Union, Callable
from . import DomAccessComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.wrappers import DomWrapper
from stractor.component_registry import component_registry
from stractor.extract_context import ExtractContext
from stractor.engine import ExtractEngine
from stractor.components.selectors import SelectorBase
from stractor.metas import DomMeta


class ComponentDomSelector(DomAccessComponentBase):

    @classmethod
    def create_from_config(cls, config: Dict, engine: ExtractEngine):

        children = config.pop('children', [])
        selectors_instances = cls.create_selectors_from_config(
            config.pop('selectors', []))
        component = cls(engine, children,
                        selectors=selectors_instances, **config)
        return component

    def __init__(self,
                 engine: ExtractEngine,
                 children: List[str],
                 selectors: List[SelectorBase]):
        super().__init__(engine, children)
        self.selectors = selectors
        self.meta = DomMeta()

    def _process(self,
                 domwrp: DomWrapper,
                 call_path: Tuple,
                 extract_context: ExtractContext)-> List[DomWrapper]:
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        input_dom = domwrp.data
        result = []
        for selector in self.selectors:
            sels = selector.process(input_dom)
            for sel in sels:
                result.append(
                    DomWrapper(
                        sel, call_path, self.meta, self.output_is_shared,
                        clone=True))
        return result
