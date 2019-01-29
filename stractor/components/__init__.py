# coding:utf-8
import uuid
from typing import List, Tuple, Dict, Any, Union

from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from stractor.component_registry import component_from_config

from stractor.utils.trie_tree import TrieTreeWithMetaData


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
            # new_path_level = str(uuid.uuid4())[:5]
            child_proc = self.engine.processors[child]
            new_path_level = str(uuid.uuid4())[:5] + ':' + child_proc.name
            for idx, processed_result in enumerate(processed_results):
                child_proc.process(
                    processed_result,
                    call_path + ((new_path_level, idx),),
                    result_context)

    def _process(self,
                 domwrp: 'DomWrapper',
                 call_path: Tuple,
                 result_context: Union[List, Dict]) -> 'DomWrapper':
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        raise NotImplementedError()
