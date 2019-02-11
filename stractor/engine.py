# coding:utf-8
from typing import Dict, Type
from lxml import etree
from html5_parser import parse

from stractor.wrappers import DomWrapper
from stractor.component_registry import (
    component_registry, component_from_config)
from stractor.extract_context import ExtractContext
from stractor.utils.dom_modifier import add_id_to_all_node
from stractor.utils.validators import validate_component_name
from stractor.exceptions import NameContainsIllegalChar
from stractor.metas import DomMeta


class ExtractEngine:
    def __init__(self, entry_point):
        self.processors = {}
        self.entry_point = entry_point
        self.is_debug = False

    def add_processor(self, name, processor):
        self.processors[name] = processor

    def extract(self, html):
        dom = parse(html)
        add_id_to_all_node(dom)
        entry_processor = self.processors[self.entry_point]
        entry_dom_is_shared = len(entry_processor.children) > 1
        print('typetypetype', type(dom))
        domwrp = DomWrapper(dom, (), DomMeta(),
                            is_shared=entry_dom_is_shared, clone=False)
        extract_ctx = ExtractContext(is_debug=self.is_debug)
        entry_processor.process(
            domwrp, ((0, f'{entry_processor.name}'),), extract_ctx)
        return extract_ctx


class ExtractEngineFactory:
    def __init__(self):
        self.processor_classes = {}

    def register_processor_class(self, name: str, cls: Type):
        self.processor_classes[name] = cls

    def create_engine_from_config(self, config: Dict) -> ExtractEngine:
        entry_point = config['entry']
        engine = ExtractEngine(entry_point)
        cfg_processors = config['processors']
        for proc_name, proc_cfg in cfg_processors.items():
            if not validate_component_name(proc_name):
                raise NameContainsIllegalChar()
            proc = component_from_config(proc_cfg, engine=engine)
            proc.name = proc_name
            engine.add_processor(proc_name, proc)
        return engine
