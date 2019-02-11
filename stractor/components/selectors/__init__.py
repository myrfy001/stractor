# coding:utf-8

from abc import abstractmethod

from lxml.etree import _Element

from .. import ComponentBase


class SelectorBase(ComponentBase):
    def __init__(self, rule: str):
        self.rule = rule

    @abstractmethod
    def process(self, dom: _Element):
        pass
