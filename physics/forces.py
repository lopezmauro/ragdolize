
# -*- coding: utf-8 -*-
"""Particle system Forces objects

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
from ..math_utils import Vector

class Force(object):
    """base Force object abstraction 
    """
    def solve(self):
        """this method will be called for the dynamic system to solve the force added
        to the particles, should be override by each Force instance
        """
        raise NotImplementedError

class ConstantForce(Force):
    """apply a constant force to the particles
    """
    def __init__(self, partciles, vector=[0,0,0], strenght=1.0):
        self._partciles = partciles
        self._vector = Vector(vector)
        self._strenght = float(strenght)

    def solve(self):
        for each in self._partciles:
            each.addForce(self._vector * self._strenght)

class Gravity(ConstantForce):
    """apply a constant down force to the particles
    """
    def __init__(self, partciles, strenght=.1):
        super(Gravity, self).__init__(partciles,[0,-1,0] ,strenght)