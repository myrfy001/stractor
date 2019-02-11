# coding:utf-8
component_registry: dict = {}


def component_from_config(component_desc, **kwargs):
    return component_registry[
        component_desc['!component']
    ].create_from_config(component_desc['params'], **kwargs)
