# coding:utf-8

from typing import Any


def convert_to_type(value: Any, target_type: str):
    if target_type == 'text':
        return str(value)
    elif target_type == 'int':
        return int(value)
    elif target_type == 'float':
        return float(value)
    elif target_type == 'html':
        pass
