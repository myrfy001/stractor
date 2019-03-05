# coding:utf-8

from typing import Tuple, Any

from copy import deepcopy
from lxml.etree import tostring, _Element


class FlowItemWrapperBase:
    pass


class DomWrapper(FlowItemWrapperBase):
    __slots__ = ('result', 'is_shared')

    def __init__(self, data: _Element, is_shared: bool, clone: bool):
        self.data = deepcopy(data) if clone else data
        self.is_shared = is_shared

    def clone(self, is_shared: bool):
        return self.__class__(self.data, is_shared, True)

    def to_html(self):
        return tostring(self.data).decode('utf-8')
