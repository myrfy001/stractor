# coding:utf-8
import sys
sys.path.insert(0, './')
from stractor import Extractor


def test_html_selector():
    doc1 = {
        "@a": ["b", "c$", {
            "$d": 123,
            "e": None,
            "f": 123.456,
            "g": False
        }]
    }

    rule1 = {
        "version": "1",
        "selector": {
            "name":
            "L1",
            "include": [{
                "type":
                "xpath",
                "query": [
                    "/dict[@name='root']/list[@name='@a']//value[@name='$d']//text()"
                ]
            }],
            "remove": [{
                "query": ["/html/body/div[@class='grabage']"]
            }],
            "children": []
        }
    }

    Extractor(rule1).extract(Extractor.create_doc(doc1))

    doc2 = [{
        "@a": ["b", "c$", {
            "$d": 123,
            "e": None,
            "f": 123.456,
            "g": False
        }]
    }]

    rule2 = {
        "version": "1",
        "selector": {
            "name":
            "L1",
            "include": [{
                "type":
                "xpath",
                "query": [
                    "/list/dict[@name='root']/list[@name='@a']//value[@name='$d']//text()"
                ]
            }],
            "remove": [{
                "query": ["/html/body/div[@class='grabage']"]
            }],
            "children": []
        }
    }

    Extractor(rule2).extract(Extractor.create_doc(doc2))


test_html_selector()
