# coding:utf-8
import sys
sys.path.insert(0, './')
from stractor import Extractor


def test_html_selector():
    doc = open('tests/test_cases/list.html').read()

    rule = {
        "version": "1",
        "selector": {
            "name": "L1",
            "include": [{
                "type": "xpath",
                "query": ["/html/body/div", "/html/body/div//a/@href"]
            }],
            "remove":[
                {
                    "query": ["/html/body/div[@class='grabage']"]
                }
            ],
            "children": [
                {
                    "name": "L2_cat1",
                    "include": [{"query": ["./div[@class='cat_1']"]}],
                    "children": [
                        {
                            "name": "L3",
                            "include": [{"query": [".//@href"]}]
                        }
                    ]   
                },
                {
                    "name": "L2_cat2",
                    "include": [{"query": ["./div[@class='cat_2']"]}],
                    "children": [
                        {
                            "name": "L3",
                            "include": [{"query": [".//@href"]}]
                        }
                    ]   
                }
            ]
        }
    }

    Extractor(rule).extract(Extractor.create_doc(doc))


test_html_selector()
