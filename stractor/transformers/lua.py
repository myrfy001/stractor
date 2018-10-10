# coding:utf-8

import lupa
from lupa import LuaRuntime


class LuaTransformer:
    @classmethod
    def transform(cls, rule, doc, **kwargs):
        lua = LuaRuntime(unpack_returned_tuples=False)
        handle_func = lua.eval(rule)
        ret = handle_func(doc, kwargs)
        return ret
