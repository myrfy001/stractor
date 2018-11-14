# coding:utf-8
import sys
sys.path.insert(0, './')

import json

from stractor import Extractor

import requests

resp = requests.get('https://www.feixiaohao.com/currencies/neo/')

html = resp.text

web_shooter_export = json.loads('''
{"main_data":[{"id":1,"fieldname":"root123","xpath":"","fieldtype":"f_group","children":[{"id":"aaeb39dc-02da-4bfb-a6e6-5af7d5fc7d83","label":"testtest","children":[],"fieldtype":"f_include","xpath":"/html[1]/body[1]/div[5]"},{"id":"a0c6d369-26a2-4b0f-a155-03f02bb49e8c","label":"testtest","children":[{"id":"155c1ed7-9fca-4da0-90ee-0af1e3c065e6","children":[],"fieldname":"","fieldtype":"f_include","xpath":"./div[1]/div[1]/div[2]/ul/li"},{"id":"d3cb7128-3d26-40a6-bf82-144614e08766","children":[],"fieldtype":"v_string","fieldname":"name","xpath":"./span[1]/text()"},{"id":"77fd1497-86ef-4f51-9dc9-4effae53e74d","children":[],"xpath":"./span[2]/text()","fieldname":"value","fieldtype":"v_string"}],"fieldtype":"f_group","fieldname":"head_table_basic_info"},{"id":"8bcf51b3-9910-41af-89ba-d20979cebff8","children":[],"fieldtype":"v_string","fieldname":"市值","xpath":"./div[1]/div[1]/div[1]/div[2]/div[2]/text()"}]}],"stractor_selector":{"name":"root123","include":[{"type":"xpath","query":["/html[1]/body[1]/div[5]"]}],"remove":[],"value":[{"type":"xpath","name":"市值","query":["./div[1]/div[1]/div[1]/div[2]/div[2]/text()"]}],"children":[{"name":"head_table_basic_info","include":[{"type":"xpath","name":"","query":["./div[1]/div[1]/div[2]/ul/li"]}],"remove":[],"value":[{"type":"xpath","name":"name","query":["./span[1]/text()"]},{"type":"xpath","name":"value","query":["./span[2]/text()"]}],"children":[]}]}}
''')

stractor_rule = {
    'version': '1',
    'selector': web_shooter_export['stractor_selector']
}

ret = Extractor(stractor_rule).extract(Extractor.create_doc(html))

print(ret)