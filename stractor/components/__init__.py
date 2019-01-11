# coding:utf-8
import uuid
from typing import List, Tuple, Dict, Any, Union


class ComponentBase:

    @classmethod
    def create_selectors_from_config(cls,
                                     component_registry: Dict,
                                     selectors_cfg: List[Dict]):
        selectors_instances = []
        for selector in selectors_cfg:
            selector_class = component_registry[selector['component']]
            selector_ins = selector_class.create_from_config(
                selector['params'])
            selectors_instances.append(selector_ins)
        return selectors_instances

    def __init__(self, engine: 'ExtractEngine', children: List[str]):
        self.engine = engine
        self.children = children
        self.output_is_shared = len(self.children) > 1

    def process(self, domwrps: List['DomWrapper'],
                call_path: Tuple,
                result_context: Union[List, Dict]):
        call_path = call_path + (str(uuid.uuid4()),)
        processed_results = [
            self._process(x, call_path, result_context) for x in domwrps]
        for child in self.children:
            for processed_result in processed_results:
                self.engine.processors[child].process(
                    processed_result, call_path, {})

    def _process(self,
                 domwrp: 'DomWrapper',
                 call_path: Tuple,
                 result_context: Union[List, Dict]) -> 'DomWrapper':
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        raise NotImplementedError()
