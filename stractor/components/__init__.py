# coding:utf-8
import uuid
from typing import List, Tuple, Dict, Any, Union

from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from stractor.component_registry import component_from_config
from stractor.utils.trie_tree import TrieTreeWithMetaData
from stractor.utils.inc_counter import IncCounter


uid_counter = IncCounter()


class ComponentABC(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def create_from_config(cls):
        pass

    @abstractmethod
    def process(self):
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

    def __init__(self, engine: 'ExtractEngine', children: List[str]):
        self.engine = engine
        self.children = children
        self.output_is_shared = len(self.children) > 1
        self.name = None

    def process(self, domwrps: 'DomWrapper',
                call_path: Tuple,
                result_context: TrieTreeWithMetaData):
        processed_results = self._process(domwrps, call_path, result_context)

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
                    result_context)

    def _process(self,
                 domwrp: 'DomWrapper',
                 call_path: Tuple,
                 result_context: Union[List, Dict]) -> 'DomWrapper':
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        raise NotImplementedError()
