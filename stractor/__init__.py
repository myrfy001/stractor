#coding:utf-8

from .html5gumboparser import patch_parsel
from .queries.dom import XpathQuerier, CssQuerier
from .queryitem import QueryItem
from .extractor import Extractor

patch_parsel()

QueryItem.register_querier('xpath', XpathQuerier)
QueryItem.register_querier('css', CssQuerier)
