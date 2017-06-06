#!/usr/bin/env python
# -*- coding: utf-8 -*-

def toy_question(x, param=None):
    return int(x)%2

def identity(x, param=None):
    return x

def zero(x, param=None):
    return 0

def constant(x, value):
    return value

def projection(x, index):
    return x[index]

def bigger_than(x, minimum):
    if x>minimum:
        return 1
    else:
        return 0

def smaller_than(x, maximum):
    if x<maximum:
        return 1
    else:
        return 0

def equivalent_to(x, value):
    if x==value:
        return 1
    else:
        return 0

def ranges_sort(x, ranges):
    for i, range_ in enumerate(ranges):
        if x < range_:
            return i
    return len(ranges)


class Node(object):

    def __init__(self, question=None, q_index=0, q_params=None, parent=None):
        self._question = question
        self._q_index = q_index
        self._q_params = q_params
        self._parent = parent
        self._children = []
        self._node_data = {}
        self._map_data = {}
        if parent:
            parent._children.append(self)

    @property
    def row_numbers(self):
        return self._node_data.keys()

    @property
    def child_index(self):
        child_index = 0
        try:
            for index, child in enumerate(self._parent._children):
                if self == child:
                    child_index = index
            return child_index
        except AttributeError:
            print('This node does not have a parent!')

    def __del__(self):  #Fix this!
        self._children = []
        self._parent = None
        self._question = None
        del self

    def output(self, input_):
        return self._question(input_[self._q_index], self._q_params)


if __name__ == "__main__":

    A = Node(ranges_sort,2,[0,1,2],None)
    print(A.__dict__)
    print(A.output([0,1,1.5]))

    B = Node(identity,1)
    A._children.append(B)
    print(A.output([0,1,1.5]))
    C = Node(bigger_than,1,1)
    B._children = C
    print(B.output([1,13]))
    print(C.output([1, 3]))