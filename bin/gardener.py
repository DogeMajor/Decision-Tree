#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bin.node import Node, constant, identity, zero, ranges_sort, bigger_than, smaller_than, equivalent_to
from bin.tree import Tree
from bin.dao import Dao, _process
from collections import Counter
import math


class Gardener(object):

    def __init__(self, dao, tree=None):
        self.dao = dao
        self.tree = tree

    def set_map_data(self, node, inputs):
        groups = len(node._children)
        if groups == 0:
            node._map_data = {}
        else:
            node._map_data = {i:node.output(row) for i, row in enumerate(inputs) if i in node.row_numbers}
        #OK

    def set_node_data(self, node, outputs_):
        if(node == self.tree._root):
            result = {index:output_row for index, output_row in enumerate(outputs_)}
        else:
            parent_data_map = node._parent._map_data
            child_index = 0
            for index, child in enumerate(node._parent._children):  #Make this into a property!!!
                if node == child:
                    child_index = index
            row_indicies = [index for index in parent_data_map.keys() if parent_data_map[index] == child_index]
            result = {row_index: outputs_[row_index] for row_index in row_indicies}
        node._node_data = result
        #OK

    def set_node_and_map_data(self, node, inputs, outputs):
        self.set_node_data(node, outputs)
        self.set_map_data(node, inputs)

    def update_node(self, node, inputs, outputs):
        self.set_node_and_map_data(node, inputs, outputs)
        for child in node._children:
            self.set_node_and_map_data(child, inputs, outputs)
        if(node._children == []):
            node._question = constant
            node._q_params = self.most_common_group(node)

    def most_common_group(self, node):
        node_data = node._node_data
        hist = Counter(node_data.values())
        group = max(hist, key=hist.get)
        print(hist)
        return group

    @staticmethod
    def entropy(dict):
        length = sum(list(dict.values()))
        return sum([-(x / length) * math.log(x / length) for x in list(dict.values()) if x != 0])
        # OK

    def _node_entropy(self, node):
        node_data = node._node_data
        histogram = Counter(node_data.values())
        return self.entropy(histogram)
        #OK

    def _entropy_change(self, node):
        if node._children == []:
            return 0
        else:
            children_entropies = [self._node_entropy(child) for child in node._children]
            map = node._map_data
            map_histogram = Counter(map.values())
            length = sum(list(map_histogram.values()))
            temp =list(zip(map_histogram.values(), children_entropies))
            entropy_after = sum([(item[0]/length)*item[1] for item in temp])
            entropy_before  = self._node_entropy(node)
            return entropy_after - entropy_before
            #OK

    def _choose_question(self, node, index, inputs, outputs):  #Only checks all the 'smaller_than'-functions
        #Index is fixed. Question is optimized for maximal information gain (=entropy decrease)
        node._q_index = index
        node._question = smaller_than
        entropy_changes = []
        for number in node.row_numbers:
            node._q_params = inputs[number][index]
            self.update_node(node,inputs,outputs)
            entropy_changes.append(self._entropy_change(node))
        min_index = entropy_changes.index(min(entropy_changes))
        min_number = list(node.row_numbers)[min_index]
        node._q_params = inputs[min_number][index]
        self.update_node(node, inputs, outputs)
        return node._q_params
        #OK!!! Although you should refactor!

    def _choose_question_and_index(self, node, inputs, outputs):
        entropy_changes = []
        q_params = []
        length = len(inputs[0])
        for index in range(length):
            node._q_index = index
            q_params.append(self._choose_question(node, index,inputs, outputs))
            entropy_changes.append(self._entropy_change(node))
        min_index = entropy_changes.index(min(entropy_changes))
        node._q_params = q_params[min_index]
        node._q_index = min_index
        self.update_node(node,inputs, outputs)


if __name__=="__main__":
    #--------Set up the tree and iris set -dao------------
    print(Gardener.entropy({0:50,1:50}))
    root = Node(bigger_than, 1, 3)
    child1 = Node(smaller_than, 0, 5)
    child2 = Node(zero, 0, 3)
    child21 = Node(constant, 2, 2)
    child22 = Node(constant, 2, 'C')
    child111 = Node(constant, 2, 2)
    child112 = Node(constant, 2, 'A')
    child121 = Node(constant, 2, 2)
    child122 = Node(constant, 2, 'B')
    child11 = Node(constant, 2, 1)
    tree = Tree(root)
    tree.add([0], child1)
    tree.add([0], child2)
    child12 = Node(zero, 1)
    tree.add([0, 0], child11)
    tree.add([0, 0], child12)
    tree.add([0, 1], child21)
    tree.add([0, 1], child22)
    tree.add([0, 0,0], child111)
    tree.add([0, 0,0], child112)
    tree.add([0, 0, 1], child121)
    tree.add([0, 0, 1], child122)


    iris_set = Dao('iris.data')

    inputs = iris_set._training_input()
    outputs = iris_set._training_output()
    gardener = Gardener(iris_set, tree)
    tree._root._row_numbers = list(range(len(iris_set._training_input())))
    gardener.set_node_data(tree._root, outputs)
    gardener.set_map_data(tree._root, iris_set._training_input())

    gardener.set_node_data(child1, outputs)
    gardener.set_node_data(child2, outputs)
    print(child2.row_numbers)
    gardener.set_map_data(child1, inputs)
    gardener.set_map_data(child2, inputs)

    gardener.set_node_data(child11, outputs)
    gardener.set_node_data(child12, outputs)
    gardener.set_node_data(child21, outputs)

    gardener.set_map_data(child11, inputs)
    gardener.set_map_data(child12, inputs)
    gardener.set_map_data(child21, inputs)

    gardener._choose_question(root, 1, inputs, outputs)
    print(gardener._entropy_change(root))
    print(gardener._entropy_change(root))
    gardener._choose_question(child1, 0, inputs, outputs)
    print(gardener._entropy_change(child1))
    print(child1._node_data)
    gardener._choose_question_and_index(root, inputs, outputs)
    print(gardener._entropy_change(root))
    print(gardener._entropy_change(root))
    gardener._choose_question_and_index(child1, inputs, outputs)
    print(gardener._entropy_change(child1))
    gardener._choose_question_and_index(child2, inputs, outputs)
    print(gardener._entropy_change(child2))
    gardener._choose_question_and_index(child11, inputs, outputs)
    print(gardener._entropy_change(child11))
    gardener._choose_question_and_index(child12, inputs, outputs)
    print(gardener._entropy_change(child12))
    print('entropies at the real end')
    print(gardener._node_entropy(tree._root))
    print(gardener._entropy_change(tree._root))
    print(gardener._node_entropy(child1))
    print(gardener._entropy_change(child1))
    print(gardener._node_entropy(child2))
    print(gardener._entropy_change(child2))
    print(gardener._node_entropy(child11))
    print(gardener._entropy_change(child11))
    print(gardener._node_entropy(child12))
    print(gardener._entropy_change(child12))
    print(gardener._node_entropy(child21))
    print(gardener._entropy_change(child21))
    print(gardener._node_entropy(child22))
    print(gardener._entropy_change(child22))
    print(gardener._node_entropy(child111))
    print(gardener._entropy_change(child111))
    print(gardener._node_entropy(child112))
    print(gardener._entropy_change(child112))
    print(gardener._node_entropy(child121))
    print(gardener._entropy_change(child121))
    print(gardener._node_entropy(child122))
    print(gardener._entropy_change(child122))
    gardener.update_node(child122, inputs, outputs)
    print(gardener.most_common_group(child122))
    print(gardener.most_common_group(child12))
    print(child122.__dict__)
    print(gardener.most_common_group(child122))
    print(child21.__dict__)
    print(gardener.most_common_group(child21))
    print(child2.__dict__)
    print(gardener.most_common_group(child2))
    print(child22.__dict__)
    print(gardener.most_common_group(child22))
    print(child12.__dict__)
    print(gardener.most_common_group(child12))




    #print(root.__dict__)
    #print(child1.__dict__)

