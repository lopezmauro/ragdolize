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
from ..math_utils import Vector

class Particle(object):
    def __init__(self, pos=[0,0,0], mass=1.0, damping=.99):
        self._position = Vector(pos)
        self._damping = float(damping)
        self._mass = float(mass)
        self._oldPosition = Vector(pos)
        self._pinned = False
        self._accumForce = Vector([0,0,0])
        self._bounciness = float(1.0)

    @property
    def position(self):
        return self._position

    @property
    def damping(self):
        return self._damping

    @property
    def mass(self):
        return self._mass

    @property
    def oldPosition(self):
        return self._oldPosition

    @property
    def pinned(self):
        return self._pinned

    @property
    def accumForce(self):
        return self._accumForce

    @property
    def bounciness(self):
        return self._bounciness

    def addForce(self, force):
        self._accumForce += Vector(force)

    def clearForces(self):
        self._accumForce = Vector([0,0,0])

    def updatePoint(self):
        if self._pinned:
            return
        velocity = ((self._position - self._oldPosition) * self._damping)
        self._oldPosition = Vector(self._position)
        self._position += velocity 
        self._position += (self._accumForce * self._mass)
        self.clearForces()

    def addPosition(self, vector):
        self._position = self._position + Vector(vector)

    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = Vector(position)

    def getMass(self):
        return self._mass
    
    def setMass(self, mass):
        if mass <=0.01:
            mass = 0.01
        self._mass = float(mass)

    def getPrevPosition(self):
        return self._oldPosition

    def setPrevPosition(self, pos):
        self._oldPosition = Vector(pos)

    def setPinned(self, value=True):
        self._pinned = value

    def isPinned(self):
        return self._pinned
    
    def setDamping(self, value):
        self._damping = float(value)

    def getDamping(self):
        return self._damping

    def setBounciness(self, value):
        self._bounciness = float(value)

    def getBounciness(self):
        return self._bounciness

