#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bin.node import Node, constant, identity, zero, ranges_sort, bigger_than, smaller_than, equivalent_to

class Tree(object):  #OK!

    def __init__(self, root):
        self._root = root

    def _route(self, node):
        reversed_route = []
        if node != self._root:
            while node._parent is not None:
                reversed_route.append(node.child_index)
                node = node._parent
        reversed_route.append(0)
        return list(reversed(reversed_route))

    def _goto(self, route):
        node = self._root
        if len(route) > 1:
            for number in route[1:]:
                node = node._children[number]
        return node

    def pop(self, route):
        node = self._goto(route)
        if node is not None:
            parent = node._parent
            parent._children.pop(route[-1])
            node.__del__()
            return True
        else:
            return False

    def add(self, route, node):
        parent = self._goto(route)
        if parent is not None:
            node._parent = parent
            parent._children.append(node)
            return True
        else:
            return False

    def output(self, input_):
        node = self._root
        while(node._children != []):
            index = node.output(input_)
            node = node._children[index]
        return node.output(input_)

if __name__ == "__main__":
   pass