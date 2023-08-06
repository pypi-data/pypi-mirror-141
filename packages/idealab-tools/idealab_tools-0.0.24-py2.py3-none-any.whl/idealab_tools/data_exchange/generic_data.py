# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:26:29 2020

@author: danaukes
"""
from collections import OrderedDict
class GenericData(object):
    def __init__(self, **kwargs):
        self._keys = kwargs.keys()
        for key,value in kwargs.items():
            setattr(self,key,value)
    def to_dict(self):
        output = {}
        for key in self._keys:
            output[key] = getattr(self,key)
        return output
    def to_ordered_dict(self):
        output = OrderedDict()
        for key in self._keys:
            output[key] = getattr(self,key)
        return output
