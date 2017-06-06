#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import os


def _process(row):
    temp = row.split(',')
    input = [float(temp[i]) for i in range(len(temp) - 1)]
    return input, temp[-1]

class BaseDAO(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._training_data = []

    @property
    def input_length(self):
        return len(self._training_data[0][0])

    @abc.abstractmethod
    def _read(self, *args):
        raise NotImplementedError

    def _training_input(self):
        inputs = [input for input, output in self._training_data]
        return inputs

    def _training_output(self):
        outputs = [output for input, output in self._training_data]
        return outputs


class IrisDAO(BaseDAO):

    def __init__(self, file_name):
        super(IrisDAO, self).__init__()
        self._training_data = self._read(file_name)

    def _read(self, file_name, func=_process):
        os.chdir('../data')
        with open(file_name, 'r') as file:
            data = [func(row) for row in file]
        os.chdir('../bin')
        return data


if __name__=="__main__":
    pass