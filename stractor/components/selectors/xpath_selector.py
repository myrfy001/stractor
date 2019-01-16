# coding:utf-8

from typing import List, Dict
from lxml.etree import XPath
from . import SelectorBase


class XpathSelector(SelectorBase):

    @classmethod
    def create_from_config(cls, config: Dict):
        return cls(**config)

    def __init__(self, rule: str):
        self.xpath = XPath(rule)

    def process(self, dom: '_Element') -> List:
        return self.xpath(dom)
