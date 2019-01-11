# coding:utf-8
from copy import deepcopy


class DomWrapper:
    def __init__(self, dom: '_Element', is_shared: bool, clone: bool):
        self.dom = deepcopy(dom) if clone else dom
        self.is_shared = is_shared

    def clone(self, is_shared: bool):
        return self.__class__(self.dom, is_shared, True)
