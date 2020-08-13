# -*- coding: utf-8 -*-
"""This module is mean to be used to get the main training data for train the model to be used on ml_rivets.mll node
This code is to be used on maya with numpy library

MIT License

Copyright (c) 2020 Mauro Lopez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFT
"""
from maya.api import OpenMaya as om

class Vector(object):
    def __init__(self, *args):
        if len(args)==0:
            self.array = om.MVector([0,0,0])
        if len(args)==1:
            self.array = om.MVector(*args)
        else:
            self.array = om.MVector(args)

    def magnitude(self):
        return  self.array.length()

    def normalize(self):
        return Vector(self.array.normal())
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array * other)
        return Vector(self.array * other.array)

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array / other)
        return Vector(self.array / other.array)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array/other)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array + other)
        return Vector(self.array + other.array)
        
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.array - other)
        return Vector(self.array - other.array)

    def __iter__(self):
        return iter(self.array)
    
    def __len__(self):
        return 3
    
    def __getitem__(self, key):
        return self.array[key]
    
    def __setitem__(self, key, value):
        self.array[key] = float(value)

    def __repr__(self):
        return str(self.array)

    def __neg__(self):
        return Vector(self.array * -1)


