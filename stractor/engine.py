# coding:utf-8
from typing import Dict, Type
from collections import OrderedDict
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
        entry_processor.process(domwrp, (), extract_ctx)
        import pprint
        pprint.pprint(extract_ctx)


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
            engine.add_processor(proc_name, proc)
        return engine


if __name__ == '__main__':
    import json
    from html5_parser import parse

    from stractor.components.selectors.xpath_selector import XpathSelector
    from stractor.components.dom_selector import ComponentDomSelector
    from stractor.components.dom_shaver import ComponentDomShaver
    from stractor.components.dom_value_extractor import (
        ComponentBasicDomValueExtractor)

    {
        "article": "this is article",
        "comment_group": [
            {
                "comment_text": "t1",
                "children": [
                    {
                        "comment_text": "t1-1",
                        "children": [
                            {"comment_text": "t1-1-1"}
                        ]
                    },
                    {"comment_text": "t1-2"}
                ]
            },
            {
                "comment_text": "t2",
                "children": [
                    {
                        "comment_text": "t2-1",
                        "children": [
                            {"comment_text": "t2-1-1"},
                            {"comment_text": "t2-1-2"}
                        ]
                    }
                ]
            }
        ]
    }

    html = '''
    <o>
        <article>
            this is article
        </article>
        <c id="1">
            <t>t1</t>
            <div><like>l1</like></div>
            <c id="1-1">
                <t>t1-1</t>
                <div><like>l1-1</like></div>
                <c id="1-1-1">
                    <t>t1-1-1</t>
                    <div><like>l1-1-1</like></div>
                </c>
            </c>
            <c id="1-2">
                <t>t1-2</t>
                <div><like>l1-2</like></div>
            </c>
        </c>
        <c id="2">
            <t>t2</t>
            <div><like>l2</like></div>
            <c id="2-1">
                <t>t2-1</t>
                <div><like>l2-1</like></div>
                <c id="2-1-1">
                    <t>t2-1-1</t>
                    <div><like>l2-1-1</like></div>
                </c>
                <c id="2-1-2">
                    <t>t2-1-2</t>
                    <div><like>l2-1-2</like></div>
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
                "!component":"ComponentDomSelector",
                "params":{
                    "selectors":[
                        {
                            "!component": "XpathSelector",
                            "params":{
                                "rule":"//body/o"
                            }
                        }
                    ],
                    "children":["p1", "p3"]
                }
            },
            "p1":{
                "name":"递归抽取C标签",
                "!component": "ComponentDomSelector",
                "params":{
                    "selectors":[
                        {
                            "!component": "XpathSelector",
                            "params":{
                                "rule":"./c"
                            }
                        }
                    ],
                    "children":["p2-0", "p2-1", "p1"]
                }
            },
            "p2-0":{
                "name":"评论抽取器",
                "!component": "ComponentBasicDomValueExtractor",
                "params":{
                    "group_name":"comment_group",
                    "fields":[
                        {
                            "name": "comment_text",
                            "value_type": "text",
                            "is_array": false,
                            "default_value": null,
                            "allow_missing": true,
                            "selectors":[
                                {
                                    "!component": "XpathSelector",
                                    "params":{
                                        "rule":"./t/text()"
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            "p2-1":{
                "name": "评论点赞div标签删除器",
                "!component":"ComponentDomSelector",
                "params":{
                    "selectors":[
                        {
                            "!component": "XpathSelector",
                            "params":{
                                "rule":"./div/like"
                            }
                        }
                    ],
                    "children":["p2-1-0"]
                }
            },
            "p2-1-0":{
                "name":"点赞数抽取器",
                "!component": "ComponentBasicDomValueExtractor",
                "params":{
                    "group_name":"comment_group",
                    "fields":[
                        {
                            "name": "comment_like",
                            "value_type": "text",
                            "is_array": false,
                            "default_value": null,
                            "allow_missing": true,
                            "selectors":[
                                {
                                    "!component": "XpathSelector",
                                    "params":{
                                        "rule":"./text()"
                                    }
                                }
                            ]
                        }
                    ]
                }
            },
            "p3":{
                "name":"文章抽取器",
                "!component": "ComponentBasicDomValueExtractor",
                "params":{
                    "group_name":"article_group",
                    "fields":[
                        {
                            "name": "article_text",
                            "value_type": "text",
                            "is_array": false,
                            "default_value": null,
                            "allow_missing": true,
                            "selectors":[
                                {
                                    "!component": "XpathSelector",
                                    "params":{
                                        "rule":"./article/text()"
                                    }
                                }
                            ]
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
        'ComponentBasicDomValueExtractor': ComponentBasicDomValueExtractor
    })
    extract_engine_factory = ExtractEngineFactory()
    engine = extract_engine_factory.create_engine_from_config(config)
    engine.extract(html)
