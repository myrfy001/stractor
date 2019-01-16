# coding:utf-8
from collections import OrderedDict
from typing import List, Tuple, Dict, Union, Callable
from . import DomAccessComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.utils.type_convertor import convert_to_type
from stractor.extract_context import ExtractContext
from stractor.dom_wrapper import DomWrapper
from stractor.component_registry import component_registry
from stractor.exceptions import MissingFieldError


class ComponentBasicDomValueExtractor(DomAccessComponentBase):

    @classmethod
    def create_from_config(cls, config: Dict, engine: 'ExtractEngine'):
        children = config.pop('children', [])
        config.pop('name', None)
        field_cfgs = config['fields']
        for field_cfg in field_cfgs:
            selectors_instances = cls.create_selectors_from_config(
                field_cfg.pop('selectors', []))
            field_cfg['selectors'] = selectors_instances
        component = cls(engine, children, field_cfgs)
        return component

    def __init__(self,
                 engine: 'ExtractEngine',
                 children: List[str],
                 fields: Dict[str, Dict]):
        super().__init__(engine, children)
        self.field_infos = fields

    def _process(self,
                 domwrp: 'DomWrapper',
                 call_path: Tuple,
                 extract_context: ExtractContext)-> 'DomWrapper':
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times

        result = OrderedDict()
        input_dom = domwrp.dom

        for field_info in self.field_infos:
            field_name = field_info['name']
            value_type = field_info['value_type']
            selectors = field_info['selectors']
            is_array = field_info['is_array']
            result_buf = []
            for selector in selectors:
                sels = selector.process(input_dom)
                result_buf.extend(sels)
            if not result_buf:
                if field_info['allow_missing']:
                    result_buf.append(field_info['default_value'])
                else:
                    raise MissingFieldError()
            result_buf = [convert_to_type(x, value_type) for x in result_buf]
            if not is_array:
                if result_buf:
                    result_buf = result_buf[0]
            result[field_name] = result_buf
        print(call_path, result)
        # print(call_path)
        extract_context.add_item(call_path, result)
        return result
