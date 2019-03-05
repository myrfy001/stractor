# coding:utf-8
from collections import OrderedDict
from typing import List, Tuple, Dict, Union, Callable, Optional, Any
from . import DomAccessComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.utils.type_convertor import convert_to_type
from stractor.utils.document_merge import ConflictAction, conflict_enum_map
from stractor.wrappers import DomWrapper
from stractor.component_registry import component_registry
from stractor.exceptions import MissingFieldError
from stractor.engine import ExtractEngine


class ComponentBasicDomValueExtractor(DomAccessComponentBase):

    @classmethod
    def create_from_config(cls, config: Dict, engine: ExtractEngine):
        children = config.pop('children', [])
        group_name = config.pop('group_name', None)
        merge_conflict = conflict_enum_map[
            config.pop('merge_conflict', 'recursive')]
        force_list = config.pop('force_list', True)
        field_cfgs = config['fields']
        for field_cfg in field_cfgs:
            selectors_instances = cls.create_selectors_from_config(
                field_cfg.pop('selectors', []))
            field_cfg['selectors'] = selectors_instances
        component = cls(engine, children,
                        group_name,
                        merge_conflict,
                        force_list, field_cfgs)
        return component

    def __init__(self,
                 engine: ExtractEngine,
                 children: List[Union[str, 'DomAccessComponentBase']],
                 group_name: Optional[str],
                 merge_conflict: ConflictAction,
                 force_list: bool,
                 fields: List[Dict[str, Dict]]):
        super().__init__(engine, children)
        self.field_infos = fields
        self.group_name = group_name
        self.merge_conflict = merge_conflict
        self.force_list = force_list

    def process(self, domwrp: DomWrapper)-> List[Any]:
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times

        # TODO use ordered dict, now only for test
        result = OrderedDict()
        # result = {}
        input_dom = domwrp.data

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
            return [result]
