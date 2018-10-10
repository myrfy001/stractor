# coding:utf-8

import lupa
from lupa import LuaRuntime


class LuaQuerier:
    @classmethod
    def query(cls, queries, doc, **kwargs):
        result = []
        for query in queries:
            lua = LuaRuntime(unpack_returned_tuples=False)
            handle_func = lua.eval(query)
            ret = handle_func(lupa.as_attrgetter(doc), kwargs)
            result.extend(ret)
        return result
