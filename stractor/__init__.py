#coding:utf-8

from .queries.dom import XpathQuerier, CssQuerier
from .queries.lua import LuaQuerier
from .queryitem import QueryItem
from .extractor import Extractor

from .transformer import Transformer

from .transformers.default import DefaultTransformer
from .transformers.lua import LuaTransformer

QueryItem.register_querier('xpath', XpathQuerier)
QueryItem.register_querier('css', CssQuerier)
QueryItem.register_querier('lua', LuaQuerier)

Transformer.register_transformer('default', DefaultTransformer)
Transformer.register_transformer('lua', LuaTransformer)