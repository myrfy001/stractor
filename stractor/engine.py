# coding:utf-8
from typing import Dict, Type
from lxml import etree
from html5_parser import parse

from stractor.dom_wrapper import DomWrapper
from stractor.component_registry import (
    component_registry, component_from_config)
from stractor.extract_context import ExtractContext


class ExtractEngine:
    def __init__(self, entry_point):
        self.processors = {}
        self.entry_point = entry_point

    def add_processor(self, name, processor):
        self.processors[name] = processor

    def extract(self, html):
        dom = parse(html)
        entry_processor = self.processors[self.entry_point]
        entry_dom_is_shared = len(entry_processor.children) > 1
        domwrp = DomWrapper(dom, is_shared=entry_dom_is_shared, clone=False)
        extract_ctx = ExtractContext()
        entry_processor.process(
            domwrp, ((0, f'{entry_processor.name}'),), extract_ctx)
        return extract_ctx.export_result()


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
            proc = component_from_config(proc_cfg, engine=engine)
            proc.name = proc_name
            engine.add_processor(proc_name, proc)
        return engine
