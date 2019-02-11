# coding:utf-8

import pytest

import json
from html5_parser import parse


from stractor.component_registry import component_registry
from stractor.engine import ExtractEngineFactory

from stractor.components.selectors.xpath_selector import XpathSelector
from stractor.components.dom_selector import ComponentDomSelector
from stractor.components.dom_shaver import ComponentDomShaver
from stractor.components.dom_value_extractor import (
    ComponentBasicDomValueExtractor)


def test_basic_flow():
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
        "entry": "pn1",
        "processors":{
            "pn1":{
                "name": "选中Html",
                "!component":"ComponentDomSelector",
                "params":{
                    "selectors":[
                        {
                            "!component": "XpathSelector",
                            "params":{
                                "rule":"/html"
                            }
                        }
                    ],
                    "children":["p0"]
                }
            },
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
                    "fields_group_name":"comments",
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
                    "fields_group_name":"comments",
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
                    "force_list": false,
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

    expected_output = {
        "article_text": "this is article",
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

    config = json.loads(config)

    component_registry.update({
        'XpathSelector': XpathSelector,
        'ComponentDomSelector': ComponentDomSelector,
        'ComponentDomShaver': ComponentDomShaver,
        'ComponentBasicDomValueExtractor': ComponentBasicDomValueExtractor
    })
    extract_engine_factory = ExtractEngineFactory()
    engine = extract_engine_factory.create_engine_from_config(config)
    engine.is_debug = True
    extract_ctx = engine.extract(html)
    result = extract_ctx.export_result()
    print(json.dumps(result))
    extract_ctx.export_debug_result()
