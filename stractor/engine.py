# coding:utf-8
from typing import Dict, Type
from lxml import etree
from html5_parser import parse
from itertools import zip_longest

from stractor.wrappers import DomWrapper
from stractor.component_registry import (
    component_registry, component_from_config)
from stractor.utils.dom_modifier import add_id_to_all_node
from stractor.utils.validators import validate_component_name
from stractor.utils.document_merge import merge_doc
from stractor.exceptions import NameContainsIllegalChar


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

        children_result_buf = []
        final_result = []
        step_stack = [[entry_processor,
                       domwrp,
                       final_result,
                       children_result_buf]]
        last_pop = None
        while step_stack:

            stack_top = step_stack[-1]
            (cur_proc,
             cur_input,
             parent_result_buf,
             children_result_buf) = stack_top

            if cur_proc.children:
                if last_pop is not cur_proc.children[-1]:
                    # first time visit this node
                    cur_proc_results = cur_proc.process(cur_input)
                    if not cur_proc_results:
                        # if can't extract anything, then no need to handle
                        # child and we should return
                        step_stack.pop()
                        last_pop = cur_proc
                        continue

                    # 中间结果
                    new_children_result_buf = [
                        [] for _ in range(len(cur_proc.children))]
                    stack_top[3] = new_children_result_buf
                    for cur_proc_result in reversed(cur_proc_results):
                        for idx, child_proc in enumerate(
                                reversed(cur_proc.children)):
                            step_stack.append(
                                [child_proc,
                                 cur_proc_result,
                                 new_children_result_buf[-idx-1],
                                 None])
                else:
                    # Merge
                    last_pop, _, _, children_result_buf = step_stack.pop()

                    if len(last_pop.children) == 1:
                        parent_result_buf.extend(children_result_buf[0])
                        continue

                    result = []
                    for items_to_merge in zip_longest(*children_result_buf):
                        first_item = None
                        for item in items_to_merge:
                            if item is None:
                                continue
                            if first_item is None:
                                first_item = item
                                continue
                            first_item = merge_doc(
                                first_item, item, cur_proc.merge_conflict)
                        result.append(first_item)

                    if not cur_proc.force_list and len(result) == 1:
                        result = result[0]

                    if cur_proc.group_name is not None:
                        result = {cur_proc.group_name: result}
                    parent_result_buf.append(result)

            elif not cur_proc.children:
                # 最终结果
                step_stack.pop()
                last_pop = cur_proc

                cur_proc_results = cur_proc.process(cur_input)
                for cur_proc_result in cur_proc_results:
                    if cur_proc.group_name is not None:
                        cur_proc_result = {
                            cur_proc.group_name: cur_proc_result}
                    parent_result_buf.append(cur_proc_result)

        if isinstance(final_result[0], list) and len(final_result[0]) == 1:
            return final_result[0][0]
        else:
            return final_result[0]


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
