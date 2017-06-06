#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bin.node import Node, constant, identity, zero, ranges_sort, bigger_than, smaller_than, equivalent_to
from bin.tree import Tree
from bin.dao import IrisDAO
from collections import Counter
import math


class Gardener(object):

    def __init__(self, dao):
        self.dao = dao
        self._training_input = dao._training_input()
        self._training_output = dao._training_output()

    def set_map_data(self, node):
        node._map_data = {}
        if node._children != []:
            node._map_data = {i: node.output(row) for i, row in enumerate(self._training_input) if i in node.row_numbers}

    def set_node_data(self, node):
        if node._parent == None:
            result = {index: output_row for index, output_row in enumerate(self._training_output)}
        else:
            parent_data_map = node._parent._map_data
            child_index = node.child_index
            row_indices = [index for index in parent_data_map.keys() if parent_data_map[index] == child_index]
            result = {row_index: self._training_output[row_index] for row_index in row_indices}
        node._node_data = result

    def set_node_and_map_data(self, node):
        self.set_node_data(node)
        self.set_map_data(node)

    def update_node(self, node):
        self.set_node_and_map_data(node)
        for child in node._children:
            self.set_node_and_map_data(child)
        if node._children == []:
            node._question = constant
            node._q_params = self.most_common_group(node)

    def most_common_group(self, node):
        node_data = node._node_data
        hist = Counter(node_data.values())
        group = max(hist, key=hist.get)
        return group

    @staticmethod
    def entropy(hist):
        length = sum(list(hist.values()))
        return sum([-(x / length) * math.log(x / length) for x in list(hist.values()) if x != 0])

    def _node_entropy(self, node):
        node_data = node._node_data
        histogram = dict(Counter(node_data.values()))
        return self.entropy(histogram)

    def _entropy_change(self, node):
        if node._children == []:
            return 0
        else:
            children_entropies = [self._node_entropy(child) for child in node._children]
            map_histogram = Counter(node._map_data.values())
            length = sum(list(map_histogram.values()))
            entropy_histogram = {map_histogram[child_no]: entropy for child_no, entropy in enumerate(children_entropies)}
            entropy_before = self._node_entropy(node)
            entropy_after = sum([key * value for key, value in entropy_histogram.items()]) / length
            return entropy_after - entropy_before

    def _choose_question(self, node, index):  #Only checks all the 'smaller_than'-functions
        #Index is fixed. Question is optimized for maximal information gain (=entropy decrease)
        node._q_index = index
        node._question = smaller_than
        entropy_changes = []
        for number in node.row_numbers:
            node._q_params = self._training_input[number][index]
            self.update_node(node)
            entropy_changes.append(self._entropy_change(node))
        min_index = min(range(len(entropy_changes)), key=entropy_changes.__getitem__)
        min_number = list(node.row_numbers)[min_index]
        node._q_params = self._training_input[min_number][index]
        self.update_node(node)
        return node._q_params

    def _choose_question_and_index(self, node):
        entropy_changes = []
        q_params = []
        length = len(self._training_input[0])
        for index in range(length):
            node._q_index = index
            q_params.append(self._choose_question(node, index))
            entropy_changes.append(self._entropy_change(node))
        min_index = entropy_changes.index(min(entropy_changes))
        node._q_params = q_params[min_index]
        node._q_index = min_index
        self.update_node(node)

    def _set_layer(self, S_cutoff, tree, layer_number, nodes, children_amount):  #Includes S cutoff!!!!
        for node in nodes:
            route = tree._route(node)
            if self._node_entropy(node) > S_cutoff:
                for child_number in range(children_amount):
                    tree.add(route, Node(smaller_than))
            self._choose_question_and_index(node)

    def build_tree(self, max_depth, S_cutoff):
        children_amount = 2
        root = Node(smaller_than)
        tree = Tree(root)
        self.set_node_data(tree._root)
        nodes = children = []
        nodes.append(tree._root)
        layer_number = 0
        while layer_number < max_depth and nodes != []:
            self._set_layer(S_cutoff, tree, layer_number, nodes, children_amount)
            children_lists = [node._children for node in nodes]
            children = [child for node_children in children_lists for child in node_children]
            nodes = children
            layer_number += 1
        for child in children:
            self.update_node(child)
        return tree


if __name__ == "__main__":
    pass