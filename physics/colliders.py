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
class Collider(object):
    """base collider abstraction 
    """
    def solve(self):
        """this method will be called for the dynamic system to solve the collision
        should be override by each collider instance
        """
        raise NotImplementedError
    def reset(self):
        return

class GroundCollider(Collider):
    """simple plane collider object
    """
    def __init__(self, partciles, bouncinnes=0.1, friction=.9, height=0.0):
        self.bouncinnes = bouncinnes
        self.friction = friction
        self.height = float(height)
        self.particles = partciles

    def solve(self):
        """if the particle is below the plane height it will bounce usiong the 
        opocite velocity scaled by the bounciness argument
        """
        for each in self.particles:
            if each.isPinned():
                continue
            currPos = each.getPosition()
            if currPos[1] < self.height:
                prevPos = each.getPrevPosition()
                velocity = (currPos - prevPos) * self.friction
                currPos[1] = self.height
                each.setPosition(currPos)
                prevPos[1] = currPos[1]+(velocity[1] * each.getBounciness() * self.bouncinnes)
                each.setPrevPosition(prevPos)
