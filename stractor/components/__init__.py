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

    def __init__(self, engine: ExtractEngine,
                 children: List[Union[str, 'DomAccessComponentBase']]):
        self.engine = engine
        self.children = children
        self.output_is_shared = len(self.children) > 1
        self.name = None

    def process(self, valwrps: Union[DomWrapper, ResultWrapper]):
        raise NotImplementedError()
