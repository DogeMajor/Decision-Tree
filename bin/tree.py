#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bin.node import Node, constant, identity, zero, ranges_sort, bigger_than, smaller_than, equivalent_to

class Tree(object):  #OK!

    def __init__(self, root):
        self._root = root
        self._structure = {0: [[0]]}  #normal indexing!!!
        #OK

    def _route(self, node):   #Gives the route to the node OBS! Does not check if the node belongs to the tree!!!
        reversed_route = []
        if node == self._root:
            reversed_route.append(0)
        else:
            while node._parent != None:
                reversed_route.append(node.child_index)
                node = node._parent
            reversed_route.append(0)
        return list(reversed(reversed_route))
        #OK!

    def _goto(self, route):   #route has the structure: [i_0, i_1, ...],every index corresponds with a layer
        node = self._root
        if len(route) > 1:
            for number in route[1:]:
                node = node._children[number]
            #return node
        return node
        #OK

    def pop(self, route):  #There's no check that this is the end node!!!!
        node = self._goto(route)
        if node != None:
            parent = node._parent
            parent._children.pop(route[-1])
            node.__del__()
            del node
            return True
        else:
            return False
        #OK

    def add(self, route, node):
        parent = self._goto(route)
        if parent != None:
            node._parent = parent
            parent._children.append(node)
            return True
        else:
            return False
        #OK

    def output(self, input_):  #len(input_) == 1 OBS! This does return a node and a number!!!
        node = self._root
        index = None
        while(node._children != []):
            index = node.output(input_)
            node = node._children[index]
        return node, node.output(input_)
        #OK  Jiihhuu!!!


if __name__=="__main__":
   pass