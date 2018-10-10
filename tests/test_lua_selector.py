# coding:utf-8
import sys
sys.path.insert(0, './')
from stractor import Extractor


def test_html_selector():
    doc = open('tests/test_cases/list.html').read()

    rule = {
        "version": "1",
        "selector": {
            "name":
            "L1",
            "include": [{
                "type":
                "lua",
                "query": [
                    """
                    function(doc, kwargs)
                        print("---")
                        return doc.xpath("//div//text()")
                    end
                """
                ]
            }],
            "remove": [{
                "query": ["/html/body/div[@class='grabage']"]
            }],
        },
        "transformer": {
            "type":
            "lua",
            "rule":
            """
                function(doc, kwargs)
                    print("---")
                    print(doc["name"])
                    return doc["name"]
                end
            """
        }
    }

    Extractor(rule).extract(Extractor.create_doc(doc))


test_html_selector()
