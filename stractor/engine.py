# coding:utf-8
from typing import Dict, Type
from lxml import etree
from html5_parser import parse

from stractor.dom_wrapper import DomWrapper
from stractor.component_registry import component_registry


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
        entry_processor.process([domwrp], (), {})


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
            component = proc_cfg['component']
            children = proc_cfg.get('children', [])
            params = proc_cfg.get('params', {})
            proc = component_registry[component].create_from_config(
                engine=engine, children=children, config=params)
            engine.add_processor(proc_name, proc)
        return engine


if __name__ == '__main__':
    import json
    from html5_parser import parse

    from stractor.selectors.xpath_selector import XpathSelector
    from stractor.components.dom_selector import ComponentDomSelector
    from stractor.components.dom_shaver import ComponentDomShaver
    from stractor.components.dom_value_extractor import (
        ComponentDomValueExtractor)

    html = '''
    <o>
        <c id="1">
            <t>t1</t>
            <c id="1-1">
                <t>t1-1</t>
                <c id="1-1-1">
                    <t>t1-1-1</t>
                </c>
            </c>
            <c id="1-2">
                <t>t1-2</t>
            </c>
        </c>
        <c id="2">
            <t>t2</t>
            <c id="2-1">
                <t>t2-1</t>
                <c id="2-1-1">
                    <t>t2-1-1</t>
                </c>
                <c id="2-1-2">
                    <t>t2-1-2</t>
                </c>
            </c>
        </c>
    </o>
    '''

    config = """
    {
        "entry": "p0",
        "processors":{
            "p0":{
                "name": "选中Body",
                "component":"ComponentDomSelector",
                "params":{
                    "selectors":[
                        {
                            "component": "XpathSelector",
                            "params":{
                                "rule":"//body/o"
                            }
                        }
                    ]
                },
                "children":["p1"]
            },
            "p1":{
                "name":"递归抽取C标签",
                "component": "ComponentDomSelector",
                "params":{
                    "selectors":[
                        {
                            "component": "XpathSelector",
                            "params":{
                                "rule":"./c"
                            }
                        }
                    ]
                },
                "children":["p2", "p1"]
            },
            "p2":{
                "name":"值抽取器",
                "component": "ComponentDomValueExtractor",
                "params":{
                    "selectors":[
                        {
                            "component": "XpathSelector",
                            "params":{
                                "rule":"./t/text()"
                            }
                        }
                    ]
                }
            }
        }
    }
    """

    config = json.loads(config)

    component_registry.update({
        'XpathSelector': XpathSelector,
        'ComponentDomSelector': ComponentDomSelector,
        'ComponentDomShaver': ComponentDomShaver,
        'ComponentDomValueExtractor': ComponentDomValueExtractor
    })
    extract_engine_factory = ExtractEngineFactory()
    engine = extract_engine_factory.create_engine_from_config(config)
    engine.extract(html)
