#coding:utf-8
from lxml import etree
from .queryitem import QueryItem


class Selector:
    def __init__(self, selector):
        self.name = selector['name']
        self.include = [QueryItem(x) for x in selector.get('include', [])]
        self.remove = [QueryItem(x) for x in selector.get('remove', [])]
        self.children = selector.get('children')
        if self.children is not None:
            self.children = [Selector(x) for x in self.children]

    def select(self, doc, **kwargs):
        need_remove_nodes = set()
        selected_nodes = set()
        result = []

        # 首先建立节点黑名单，被remove选中的节点都放入黑名单
        for remove in self.remove:
            rem_ret = remove.query(doc, **kwargs)
            for query_result in rem_ret:
                need_remove_nodes.add(query_result.root)

        # 对于每个选中的节点，一路向上直到根节点，若中间遇到给名单节点，则移除该结果，同时该
        # 结果指向根节点路径上所有的节点也被加入黑名单，通过扩大黑名单，有助于提前结束搜索。
        # 同理，若一个结果可以成功抵达根节点，表明该条路径没有被移除，其通向根节点路径上每一
        # 个节点都加入白名单，之后其他节点向上寻找过程中若遇到白名单节点，则可以提前停止搜寻。
        for include in self.include:
            inc_ret = include.query(doc, **kwargs)
            for query_result in inc_ret:
                node = query_result.root
                path_to_top = []
                # 循环条件：达到根节点或遇到白名单节点
                while node is not None and node not in selected_nodes:
                    path_to_top.append(node)
                    if node in need_remove_nodes:
                        for nod in path_to_top:
                            need_remove_nodes.add(nod)
                        break

                    node = node.getparent()
                else:
                    for nod in path_to_top:
                        selected_nodes.add(nod)
                    result.append(query_result)

        print(result)

        if self.children:
            for child in self.children:
                child.select(inc_ret[0])
