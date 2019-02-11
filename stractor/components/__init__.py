# coding:utf-8
import uuid
from typing import List, Tuple, Dict, Any, Union

from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from stractor.component_registry import component_from_config
from stractor.utils.inc_counter import IncCounter
from stractor.extract_context import ExtractContext, ResultWrapper
from stractor.wrappers import DomWrapper
from stractor.engine import ExtractEngine


uid_counter = IncCounter()


class ComponentABC(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def create_from_config(cls, config: Dict, engine: ExtractEngine):
        pass


class ComponentBase(ComponentABC):
    pass


class DomAccessComponentBase(ComponentBase):
    @classmethod
    def create_selectors_from_config(cls, selectors_cfg: List[Dict]):
        return [
            component_from_config(selector)
            for selector in selectors_cfg
        ]

    def __init__(self, engine: ExtractEngine, children: List[str]):
        self.engine = engine
        self.children = children
        self.output_is_shared = len(self.children) > 1
        self.name = None

    def process(self, valwrps: Union[DomWrapper, ResultWrapper],
                call_path: Tuple,
                extract_context: ExtractContext):
        processed_results = self._process(valwrps, call_path, extract_context)

        for processed_result in processed_results:
            # only leaf node can save result to extract context
            # in some case, process can modify the extract context by
            # itself and return None, in that case, we won't add the
            # result again
            if (not self.children) and isinstance(
                    processed_result, ResultWrapper):
                extract_context.add_item(processed_result)

            extract_context.add_debug_item(
                call_path,
                processed_result,
                processed_result.meta)

        for child in self.children:
            child_proc = self.engine.processors[child]
            new_path_level = uid_counter.get_next_str() + ':' + child_proc.name
            for idx, processed_result in enumerate(processed_results):
                child_proc.process(
                    processed_result,
                    # the format of call_path is designed for sorting in
                    # merging step, idx is used for grouping items, each idx
                    # will be an item in the resulting list. Items with the
                    # same idx will be berged into a dict, because
                    # new_path_level is monotonic and is the secondary sorting
                    # key, the merging order is same with the extraction order
                    call_path + ((idx, new_path_level),),
                    extract_context)

    def _process(self,
                 valwrp: Union[DomWrapper, ResultWrapper],
                 call_path: Tuple,
                 extract_context: ExtractContext
                 ) -> Union[DomWrapper, ResultWrapper]:
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        raise NotImplementedError()
