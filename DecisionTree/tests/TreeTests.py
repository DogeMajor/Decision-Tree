#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bin.tree import Tree
from bin.node import Node, toy_question, identity, zero, smaller_than, bigger_than, constant
import unittest


class TreeTest(unittest.TestCase):

    def setUp(self):  #Incidentally his tests Tree.add() as well
        self.root = Node(bigger_than,1,2)
        self.child1 = Node(smaller_than,0,1)
        self.child2 = Node(zero,0,)

        self.child11 = Node(constant,2,1)
        self.child12 = Node(zero, 1)
        self.child21 = Node(constant, 2, 2)
        self.tree = Tree(self.root)
        self.tree.add([0],self.child1)
        self.tree.add([0], self.child2)
        self.tree.add([0, 0], self.child11)
        self.tree.add([0, 0], self.child12)
        self.tree.add([0, 1], self.child21)


    def test_goto(self):
        #print(self.tree._goto([0, 0, 0]))
        self.assertEqual(self.tree._goto([0, 0, 0]), self.child11)
        self.assertEqual(self.tree._goto([0, 0, 1]), self.child12)
        self.assertEqual(self.tree._goto([0, 1, 0]), self.child21)

    def test_pop(self):
        self.assertTrue(self.tree.pop([0,0,1]))
        #print(self.child12._parent)
        self.assertEqual(None, self.child12._parent)

    def test_output(self):
        x0 = [1, .1, 14]
        x1 = [.5, 0, 15]
        x2 = [1.5, 2.1, 3.5]
        self.assertEqual(self.tree.output(x0), (self.child11,1))
        self.assertEqual(self.tree.output(x1), (self.child12, 0))
        self.assertEqual(self.tree.output(x2), (self.child21, 2))


    def tearDown(self):
        del self.root
        del self.child1
        del self.child2
        del self.child11
        del self.child12
        del self.child21
        del self.tree



if __name__=="__main__":
    #print(unittest.__dict__)
    unittest.main()