#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bin.node import Node, toy_question, identity, zero, smaller_than, bigger_than, constant
from bin.tree import Tree
from bin.dao import IrisDAO
from bin.gardener import Gardener
import unittest


class GardenerTest(unittest.TestCase):

    def setUp(self):
        self.root = Node(smaller_than,2,4.4)
        self.child1 = Node(constant)
        self.child2 = Node(smaller_than)
        self.tree = Tree(self.root)
        self.tree.add([0], self.child1)
        self.tree.add([0], self.child2)
        self.irisdao = IrisDAO('iris.data')
        self.gardener = Gardener(self.irisdao)

    def test_set_node_and_map_data(self):
        self.gardener.set_node_and_map_data(self.root)
        self.assertEqual(self.root._node_data[51], 'Iris-versicolor\n')
        self.assertEqual(self.root._map_data[57], 1)

    def test_update_node(self):
        self.gardener.update_node(self.root)
        self.assertEqual(self.child1._node_data[104], 'Iris-virginica\n')

    def test_node_entropy(self):
        self.gardener.set_node_and_map_data(self.root)
        self.assertEqual(self.gardener._node_entropy(self.root), 1.0986122886681096)

    def test_entropy_change(self):
        self.gardener.update_node(self.root)
        self.assertEqual(self.gardener._entropy_change(self.root), -0.7803552045207032)

    def test_choose_question(self):
        self.root._q_index = 1
        self.gardener.update_node(self.root)
        self.gardener._choose_question(self.root, 2)
        self.assertEqual(self.gardener._entropy_change(self.root), -0.7803552045207032)
        self.assertEqual(self.child1._node_data[104], 'Iris-virginica\n')

    def test_build_tree(self):
        tree = self.gardener.build_tree(5,0.5)
        node = tree._goto([0, 1, 0])
        self.assertEqual(set(node._node_data.values()), {'Iris-versicolor\n'})
        self.assertEqual(len(node._node_data), 25)

    def tearDown(self):
        del self.root
        del self.tree
        del self.child1
        del self.child2
        del self.irisdao
        del self.gardener


if __name__ == "__main__":
    unittest.main()