# coding:utf-8
from typing import List, Tuple, Dict, Union, Callable
from . import ComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.dom_wrapper import DomWrapper
from stractor.component_registry import component_registry


class ComponentDomValueExtractor(ComponentBase):

    @classmethod
    def create_from_config(cls, engine: 'ExtractEngine',
                           children: List[str], config: Dict):
        selectors_instances = cls.create_selectors_from_config(
            component_registry, config.pop('selectors', [])
        )
        component = cls(engine, children,
                        selectors=selectors_instances,
                        **config)
        return component

    def __init__(self,
                 engine: 'ExtractEngine',
                 children: List[str],
                 selectors: List['SelectorBase']):
        super().__init__(engine, children)
        self.selectors = selectors

    def _process(self,
                 domwrp: 'DomWrapper',
                 call_path: Tuple,
                 result_context: Union[List, Dict])-> 'DomWrapper':
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        input_dom = domwrp.dom
        for selector in self.selectors:
            sels = selector.select(input_dom)
            print(sels, call_path)
