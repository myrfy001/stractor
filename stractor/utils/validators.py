# coding:utf-8
import re

illegal_component_name_chars = re.compile(
    r'''[ ~`!@#$%^&*()+={}[\]|\\;:'"<>,.?/]+?''')


def validate_component_name(name):
    return illegal_component_name_chars.search(name) is None
