import json


def node_sorter(nodea, nodeb):
    if type(nodea) is dict or type(nodeb) is dict:
        return True
    else:
        return nodea < nodeb


class Node:
    predicate = node_sorter

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return Node.predicate(self.obj, other.obj)


class SortJson:
    def __init__(self, jsn, predicate):
        self.jsn = jsn
        Node.predicate = predicate
        self._sorted = self._sort(self.jsn)

    def _sort(self, jsn):
        if type(jsn) is dict:
            res = {}
            nodes = []
            for k, v in jsn.items():
                v = self._sort(v)
                nodes.append(Node((k, v)))

            nodes.sort()
            for itm in nodes:
                res[itm.obj[0]] = itm.obj[1]
            return res
        elif type(jsn) is list:
            nodes = []
            for itm in jsn:
                itm = self._sort(itm)
                nodes.append(Node(itm))
            nodes.sort()
            res = []
            for node in nodes:
                res.append(node.obj)
            return res
        else:
            return jsn

    def get_sorted(self):
        return self._sorted


def sort_from_file(file, predicate=node_sorter):
    with open(file) as f:
        jj = json.load(f)
    return SortJson(jj, predicate).get_sorted()


def sort_from_dict(obj, predicate=node_sorter):
    return SortJson(obj, predicate).get_sorted()


def sort_from_string(string, predicate=node_sorter):
    return SortJson(json.loads(string), predicate).get_sorted()
