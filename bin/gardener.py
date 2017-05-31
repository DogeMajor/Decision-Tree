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
        self._training_input = dao._training_input()
        self._training_output = dao._training_output()

    def set_map_data(self, node):
        groups = len(node._children)
        if groups == 0:
            node._map_data = {}
        else:
            node._map_data = {i:node.output(row) for i, row in enumerate(self._training_input) if i in node.row_numbers}
        #OK

    def set_node_data(self, node):
        if(node == self.tree._root):
            result = {index:output_row for index, output_row in enumerate(self._training_output)}
        else:
            parent_data_map = node._parent._map_data
            child_index = node.child_index
            row_indicies = [index for index in parent_data_map.keys() if parent_data_map[index] == child_index]
            result = {row_index: self._training_output[row_index] for row_index in row_indicies}
        node._node_data = result
        #OK

    def set_node_and_map_data(self, node):
        self.set_node_data(node)
        self.set_map_data(node)

    def update_node(self, node):
        self.set_node_and_map_data(node)
        for child in node._children:
            self.set_node_and_map_data(child)
        if(node._children == []):
            node._question = constant
            node._q_params = self.most_common_group(node)

    def most_common_group(self, node):
        node_data = node._node_data
        hist = Counter(node_data.values())
        group = max(hist, key=hist.get)
        #print('most_common_group: histogram',hist)
        return group

    @staticmethod
    def entropy(dict):
        length = sum(list(dict.values()))
        return sum([-(x / length) * math.log(x / length) for x in list(dict.values()) if x != 0])
        # OK

    def __node_histogram(self, node):   #For testing only!!!
        node_data = node._node_data
        return dict(Counter(node_data.values()))

    def _node_entropy(self, node):
        node_data = node._node_data
        histogram = dict(Counter(node_data.values()))
        #print('histogram, S',histogram,self.entropy(histogram))
        return self.entropy(histogram)
        #OK

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
            #OK

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
        #OK!!! Although you should refactor!

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
        #print('entropy changes sorted by indicies',entropy_changes)
        self.update_node(node)

    def _set_layer(self, layer_number, nodes, children_amount):
        for node in nodes:
            #children = [Node(smaller_than) for child_number in range(children_amount)]
            route = self.tree._route(node)
            for child_number in range(children_amount):
                self.tree.add(route, Node(smaller_than))

            #print(node._children)

            self._choose_question_and_index(node)
            print('first child, hist and delta(S), S', self.__node_histogram(node._children[0]),
                  self._entropy_change(node._children[0]),self._node_entropy(node._children[0]))
            print('second child, hist and delta(S), S', self.__node_histogram(node._children[1]),
                  self._entropy_change(node._children[1]),self._node_entropy(node._children[1]))
            print('node, hist and delta(S), S', self.__node_histogram(node), self._entropy_change(node),self._node_entropy(node))

    def _build_tree(self, max_depth):
        children_amount = 2
        #self.tree._root = Node(smaller_than)
        self.set_node_data(self.tree._root)
        print('root',self.tree._root)
        nodes = []
        nodes.append(self.tree._root)
        children = []

        for layer_number in range(max_depth):
            print('layer_number', layer_number)

            self._set_layer(layer_number, nodes, children_amount)
            children_lists = [node._children for node in nodes]
            children = [child for node_children in children_lists for child in node_children]
            print('layer_number, children', layer_number, len(children), children)
            nodes = children


if __name__=="__main__":


    iris_set = Dao('iris.data')
    root = Node(smaller_than)
    tree = Tree(root)
    gardener = Gardener(iris_set, tree)
    gardener._build_tree(2)
    root = gardener.tree._root
    #test = gardener.tree._goto([0,1,0,0])
    #print(test.__dict__)
    #print(gardener.most_common_group(root))
    #print(root._children[0].__dict__)
    #print(root._children[1].__dict__)


    #print(root.__dict__)
    #print(child1.__dict__)

