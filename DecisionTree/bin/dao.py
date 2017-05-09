#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import numpy as np
import math


def _process(row):   #These can be moved into a separate module if needed
    temp = row.split(',')
    input = [float(temp[i]) for i in range(len(temp) - 1)]
    return input, temp[-1]

def process(row):
    temp = row.split(',')
    result = [float(temp[i]) for i in range(len(temp)-1)].append(temp[-1])
    return result

class Dao(object):

    def __init__(self, file_name):
        #self._training_input, self._training_output  = self._read(file_name)
        self._training_data = self._read(file_name)

    def _read(self, file_name, func=_process):
        with open(file_name, 'r') as file:
            data = [func(row) for row in file]
        return data

    def _training_input(self):
        inputs = [input for input, output in self._training_data]
        return inputs

    def _training_output(self):
        outputs = [output for input, output in self._training_data]
        return outputs

    def _data_groups(self): #Not needed
        data = self._training_data
        results = [result for inputs, result in data]
        result_set = set(results)
        print(result_set)
        data_groups = {i: results[i] for i in range(len(results))}
        return data_groups

if __name__=="__main__":
    iris_set = Dao('iris.data')
    print(iris_set._data_groups())
    print(iris_set._training_input())
    print('yes!')

