# coding:utf-8
import sys
sys.path.insert(0, './')
from stractor import Extractor


def test_html_selector():
    doc = open('./区块链_钛媒体官方网站.htm').read()

    rule = {
    "version": "1",
    "selector": {
        "name": "root",
        "include": [{"type": "xpath", "query": ["/html/body"]}],
        "remove":[],
        "children": [
            {
                "name": "文章简介分组",
                "include": [{"query": [".//div[@class='user-article-list']/div/ul/li"]}], 
                "children": [
                    {"name": "文章标题", "include":[{ "query": [".//h3/a/text()"]}]},
                    {"name": "文章链接", "include":[{"query": [".//h3/a/@href"]}]},
                    {"name": "摘要", "include":[{"query": [".//p[@class='intro']//text()"]}]}
                ] 
            },
            {
                "name":"翻页链接",
                "include":[{"query": [".//ul[@class='pagination']//@href"]}]
            }
        ]
    }
}

    print(Extractor(rule).extract(Extractor.create_doc(doc)))


test_html_selector()
