# coding:utf-8
from html5_parser import parse
import parsel


def create_root_node(text, parser_cls, base_url=None):
    """Create root node for text using given parser class.
    """
    return parse(text)


def patch_parsel():
    parsel.selector.create_root_node = create_root_node
