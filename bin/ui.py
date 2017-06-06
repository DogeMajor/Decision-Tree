#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bin.node import Node, constant, identity, zero, ranges_sort, bigger_than, smaller_than, equivalent_to
from bin.tree import Tree
from bin.dao import IrisDAO
from collections import Counter
from bin.gardener import Gardener

class UI(object):

    def __init__(self, dao):
        self._gardener = Gardener(dao)
        self._max_depth = dao.input_length
        self._tree = None

    def set_up_tree(self, S_cutoff):
        self._tree = self._gardener.build_tree(self._max_depth, S_cutoff)

    def group(self, input):
        output = [self._tree.output(input_vector) for input_vector in input]
        return output

if __name__ == "__main__":

    iris_set = IrisDAO('iris.data')
    ui = UI(iris_set)
    ui.set_up_tree(0.5)
    input = iris_set._training_input()
    print(input)
    print(ui.group(input))