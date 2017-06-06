#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bin.dao import BaseDAO, IrisDAO
import unittest

class DAOTest(unittest.TestCase):

    def setUp(self):
        self.basedao = BaseDAO()
        self.irisdao = IrisDAO('iris.data')

    def test_training_input(self):
        self.assertEqual(self.irisdao._training_input()[1], [4.9, 3.0, 1.4, 0.2])
        self.assertEqual(self.basedao._training_input(), [])

    def test_training_output(self):
        self.assertEqual(self.irisdao._training_output()[51], 'Iris-versicolor\n')
        self.assertEqual(self.basedao._training_output(), [])

    def tearDown(self):
        del self.basedao
        del self.irisdao


if __name__ == "__main__":
    unittest.main()