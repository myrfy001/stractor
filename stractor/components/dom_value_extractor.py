# coding:utf-8
from collections import OrderedDict
from typing import List, Tuple, Dict, Union, Callable, Optional
from . import DomAccessComponentBase
from stractor.utils.dom_modifier import drop_tree, drop_tag
from stractor.utils.type_convertor import convert_to_type
from stractor.extract_context import ExtractContext, ResultWrapper
from stractor.wrappers import DomWrapper
from stractor.component_registry import component_registry
from stractor.exceptions import MissingFieldError
from stractor.metas import ResultMeta
from stractor.engine import ExtractEngine


class ComponentBasicDomValueExtractor(DomAccessComponentBase):

    @classmethod
    def create_from_config(cls, config: Dict, engine: ExtractEngine):
        children = config.pop('children', [])
        fields_group_name = config.pop('fields_group_name', None)
        merge_conflict = config.pop('merge_conflict', 'recursive')
        force_list = config.pop('force_list', True)
        field_cfgs = config['fields']
        for field_cfg in field_cfgs:
            selectors_instances = cls.create_selectors_from_config(
                field_cfg.pop('selectors', []))
            field_cfg['selectors'] = selectors_instances
        component = cls(engine, children,
                        fields_group_name,
                        merge_conflict,
                        force_list, field_cfgs)
        return component

    def __init__(self,
                 engine: ExtractEngine,
                 children: List[str],
                 fields_group_name: Optional[str],
                 merge_conflict: str,
                 force_list: bool,
                 fields: List[Dict[str, Dict]]):
        super().__init__(engine, children)
        self.field_infos = fields
        self.fields_group_name = fields_group_name
        self.merge_conflict = merge_conflict
        self.force_list = force_list

        result_meta = ResultMeta()
        result_meta.fields_group_name = fields_group_name
        result_meta.merge_conflict = merge_conflict
        result_meta.force_list = force_list
        self.result_meta = result_meta

    def _process(self,
                 domwrp: DomWrapper,
                 call_path: Tuple,
                 extract_context: ExtractContext)-> List[ResultWrapper]:
        # Process function should be idempotent, because _process will be
        # called on a single instance for multi times
        try:
            result = OrderedDict()
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

        finally:
            # Because at trie tree processing stage, the order and count of the results is very important for merging fields, we must make sure that no matter
            return [
                ResultWrapper(
                    call_path=call_path,
                    data=result,
                    meta=self.result_meta,
                    is_shared=self.output_is_shared,
                    clone=False)
            ]
