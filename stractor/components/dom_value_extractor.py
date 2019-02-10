# coding:utf-8
from collections import OrderedDict
from typing import List, Tuple, Dict, Union, Callable, Optional
from . import DomAccessComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.utils.type_convertor import convert_to_type
from stractor.extract_context import ExtractContext
from stractor.dom_wrapper import DomWrapper
from stractor.component_registry import component_registry
from stractor.exceptions import MissingFieldError
from stractor.result_meta import ResultMeta


class ComponentBasicDomValueExtractor(DomAccessComponentBase):

    @classmethod
    def create_from_config(cls, config: Dict, engine: 'ExtractEngine'):
        children = config.pop('children', [])
        default_parent_name = config.pop('default_parent_name', None)
        force_list = config.pop('force_list', True)
        field_cfgs = config['fields']
        for field_cfg in field_cfgs:
            selectors_instances = cls.create_selectors_from_config(
                field_cfg.pop('selectors', []))
            field_cfg['selectors'] = selectors_instances
        component = cls(engine, children,
                        default_parent_name,
                        force_list, field_cfgs)
        return component

    def __init__(self,
                 engine: 'ExtractEngine',
                 children: List[str],
                 default_parent_name: Optional[str],
                 force_list: bool,
                 fields: List[Dict[str, Dict]]):
        super().__init__(engine, children)
        self.field_infos = fields
        self.default_parent_name = default_parent_name
        self.force_list = force_list

        result_meta = ResultMeta()

        fields_to_parent_fields_name_map = {}
        for field in fields:
            fields_to_parent_fields_name_map[field['name']] = field.get(
                'parent_name', default_parent_name)

        result_meta.fields_to_parent_fields_name_map = (
            fields_to_parent_fields_name_map)

        result_meta.force_list = force_list
        self.result_meta = result_meta

    def _process(self,
                 domwrp: 'DomWrapper',
                 call_path: Tuple,
                 extract_context: ExtractContext)-> 'DomWrapper':
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        try:
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
                    if field_info.get('allow_missing', True):
                        result_buf.append(
                            field_info.get('default_value', None))
                    else:
                        raise MissingFieldError()
                result_buf = [convert_to_type(x, value_type)
                              for x in result_buf]

                # missing value is handled above
                if not is_array:
                    result_buf = result_buf[0]
                result[field_name] = result_buf

        finally:
            # Because at trie tree processing stage, the order and count of the results is very important for merging fields, we must make sure that no matter
            print(call_path, result)
            extract_context.add_item(call_path, result, self.result_meta)
            return result
