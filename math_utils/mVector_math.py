# -*- coding: utf-8 -*-
"""This module has Vector object using openMaya.api

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
    """generic vector operation done with maya api
    """
    def __init__(self, *args):
        if len(args)==0:
            self.array = om.MVector([0,0,0])
        if len(args)==1:
            self.array = om.MVector(*args)
        else:
            self.array = om.MVector(args)

    def magnitude(self):
        """return distance between the initial point and the end point
        Returns:
            float: length of the vector
        """
        return  self.array.length()

    def normalize(self):
        """scale each value proportionaly to get a vector with the same direction
        but with a magnitude of 1
        Returns:
            Vector: vector with magnitude 1
        """
        return Vector(self.array.normal())
    
    def __mul__(self, other):
        """override the multiplication operador (*)
        Args:
            other (Vector/scalar): multiply current vetor by an scalar or other Vector
        Returns:
            Vector
        """
        if isinstance(other, (int, float)):
            return Vector(self.array * other)
        return Vector(self.array * other.array)

    def __div__(self, other):
        """override the division operador (/)
        Args:
            other (Vector/scalar): divide current vetor by an scalar or other Vector
        Returns:
            Vector
        """       
        if isinstance(other, (int, float)):
            return Vector(self.array / other)
        return Vector(self.array / other.array)
    
    def __truediv__(self, other):
        """override the division operador (/)
        Args:
            other (Vector/scalar): divide current vetor by an scalar or other Vector
        Returns:
            Vector
        """
        if isinstance(other, (int, float)):
            return Vector(self.array/other)

    def __add__(self, other):
        """override the addition operador (+)
        Args:
            other (Vector/scalar): sum current vector by an scalar or other Vector
        Returns:
            Vector
        """
        if isinstance(other, (int, float)):
            return Vector(self.array + other)
        return Vector(self.array + other.array)
        
    
    def __sub__(self, other):
        """override the substract operador (-)
        Args:
            other (Vector/scalar): substract current vector by an scalar or other Vector
        Returns:
            Vector
        """
        if isinstance(other, (int, float)):
            return Vector(self.array - other)
        return Vector(self.array - other.array)

    def __iter__(self):
        """override the iteration operation(for a in Vector), iterating by each vector element
        Returns:
            iter
        """
        return iter(self.array)
    
    def __len__(self):
        """override the len operation(len(Vector)), returning how many elements has
        Returns:
            int
        """
        return len(self.array)
    
    def __getitem__(self, key):
        """override the get index operation (Vector[i]), returning the element at index
        Args:
            key (int): element at index
        Returns:
            float: value at index
        """
        return self.array[key]
    
    def __setitem__(self, key, value):
        """override the setindex operation (Vector[i]), setting the element at index
        Args:
            key (int): element at index
        """
        self.array[key] = float(value)

    def __repr__(self):
        """override the string representation
        Returns:
            str: elements as string
        """
        return str(self.array)

    def __neg__(self):
        """override the negation operation (-obj)
        Returns:
            Vector: negated Vector
        """
        return Vector(self.array * -1)


