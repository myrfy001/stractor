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
from stractor.utils.document_merge import merge_doc
from stractor.exceptions import NameContainsIllegalChar
from stractor.metas import DomMeta


class ExtractEngine:
    def __init__(self, entry_point):
        self.processors = {}
        self.entry_point = entry_point
        self.is_debug = False

    def add_processor(self, id_, processor):
        self.processors[id_] = processor

    def extract(self, html):
        dom = parse(html)
        add_id_to_all_node(dom)
        entry_processor = self.processors[self.entry_point]
        entry_dom_is_shared = len(entry_processor.children) > 1
        domwrp = DomWrapper(dom, is_shared=entry_dom_is_shared, clone=False)

        result_stack = []
        step_stack = [[entry_processor, domwrp, None]]

        while step_stack:
            stack_top = step_stack[-1]
            cur_proc, cur_input, execute_result = stack_top

            print('--------------')
            print(cur_proc.name)
            for x in result_stack:
                print(x)
            if execute_result is None:
                # first time visit this node
                cur_proc_results = cur_proc.process(cur_input)
                stack_top[2] = cur_proc_results
                if not cur_proc_results:
                    result_stack.append(None)

                if cur_proc.children:
                    # 中间结果
                    for cur_proc_result in cur_proc_results:
                        for child_proc in cur_proc.children[::-1]:
                            step_stack.append(
                                [child_proc, cur_proc_result, None])
                else:
                    # 最终结果
                    result_stack.append(cur_proc_results)

            else:
                step_stack.pop()
                if len(cur_proc.children) == 1:
                    continue
                first_result = None
                for _ in range(len(cur_proc.children)):
                    if first_result is None:
                        first_result = result_stack.pop()
                        continue
                    other_result = result_stack.pop()
                    if other_result is None:
                        continue

                    print('merge', first_result, other_result)

                    first_result = merge_doc(first_result, other_result)

                result_stack.append(first_result)

        print(result_stack)
        return result_stack.pop()


class ExtractEngineFactory:
    def __init__(self):
        self.processor_classes = {}

    def register_processor_class(self, name: str, cls: Type):
        self.processor_classes[name] = cls

    def create_engine_from_config(self, config: Dict) -> ExtractEngine:
        entry_point = config['entry']
        engine = ExtractEngine(entry_point)
        cfg_processors = config['processors']
        for proc_cfg in cfg_processors:
            proc_id = proc_cfg['id']
            if not validate_component_name(proc_id):
                raise NameContainsIllegalChar()
            proc = component_from_config(proc_cfg, engine=engine)
            proc.name = proc_id
            engine.add_processor(proc_id, proc)

        # Convert the children name to children instance
        for process in engine.processors.values():
            for idx in range(len(process.children)):
                process.children[idx] = (
                    engine.processors[process.children[idx]])
        return engine
