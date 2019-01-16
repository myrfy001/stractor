# coding:utf-8

from .. import ComponentBase


class SelectorBase(ComponentBase):
    def __init__(self, rule: str):
        self.rule = rule
