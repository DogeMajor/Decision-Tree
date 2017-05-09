#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bin.node import Node, constant, identity, zero, ranges_sort, bigger_than, smaller_than, equivalent_to

class Tree(object):  #OK!

    def __init__(self, root):
        self._root = root
        self._structure = {0: [[0]]}  #normal indexing!!!
        #OK

    def _route(self, place):
        pass

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
    root = Node(bigger_than,1,2)
    child1 = Node(smaller_than,0,1)
    child2 = Node(zero,0,)
    child21 = Node(constant,2,2)
    child11 = Node(constant,2,1)

    tree = Tree(root)
    tree.add([0],child1)
    tree.add([0], child2)
    child12 = Node(zero,1)

    print(tree.add([0, 0], child11))

    #print(tree._goto([0, 0, 0]))
    print(tree.add([0, 0], child12))
    #print(tree._goto([0, 0, 1]))
    print(tree.add([0, 1], child21))
    #print(tree._goto([0, 1, 0]))
    print('child1',child1.__dict__)
    #print(tree.pop([0, 0, 1]))

    #print(tree._goto([0, 1, 0]))
    #print(tree._goto([0, 0, 1]))
    print(tree._goto([0, 0]))
    print(child12.__dict__)
    print(child12)
    print(child1)
    print('child1',child1.__dict__)


    #print(tree.output(0))
    print(root)
    print(child1)

    print(child2)

    print(child11)
    print(child12)
    print(child21)
    print('outputs:')
    x0 = [1,.1,14]
    x1 = [.5,0,15]
    x2 = [1.5, 2.1, 3.5]

    print(tree.output(x0))
    print(tree.output(x1))
    print(tree.output(x2))
    print(constant(8,3))
