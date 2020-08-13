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
import math
import numbers

class Vector(object):
    """generic vector operation done with pure python
    """
    def __init__(self, *args):
        if len(args)==0:
            self.array = (0.0, 0.0, 0.0)
        elif len(args)==1:
            self.array = args[0]
        else :
            self.array = args
        
    def magnitude(self):
        """return distance between the initial point and the end point
        Returns:
            float: length of the vector
        """
        return math.sqrt(sum( comp**2 for comp in self.array))

    def normalize(self):
        """scale each value proportionaly to get a vector with the same direction
        but with a magnitude of 1
        Returns:
            Vector: vector with magnitude 1
        """
        mag = self.magnitude()
        return Vector(*[comp/mag for comp in self.array])
    
    def inner(self, other):
        """the inner product or dot product is a way to multiply vectors together, with the result
        of this multiplication being a scalar
        Args:
            other (Vector): other vectro to multiply

        Returns:
            float: the inner product
        """
        return sum(a * b for a, b in zip(self.array, other.array))
    
    def __mul__(self, other):
        """override the multiplication operador (*)
        Args:
            other (Vector/scalar): multiply current vetor by an scalar or other Vector
        Returns:
            Vector
        """
        if isinstance(other, self.__class__):
            return self.inner(other)
        elif isinstance(other, numbers.Number):
            return Vector([a * other for a in self.array])

    def __div__(self, other):
        """override the division operador (/)
        Args:
            other (Vector/scalar): divide current vetor by an scalar or other Vector
        Returns:
            Vector
        """
        if isinstance(other, numbers.Number):
            return Vector([a / other for a in self.array])

    def __truediv__(self, other):
        """override the division operador (/)
        Args:
            other (Vector/scalar): divide current vetor by an scalar or other Vector
        Returns:
            Vector
        """
        if isinstance(other, numbers.Number):
            return Vector([a / other for a in self.array])

    def __add__(self, other):
        """override the addition operador (+)
        Args:
            other (Vector/scalar): sum current vector by an scalar or other Vector
        Returns:
            Vector
        """
        return Vector([a + b for a, b in zip(self.array, other.array)])
        
    
    def __sub__(self, other):
        """override the substract operador (-)
        Args:
            other (Vector/scalar): substract current vector by an scalar or other Vector
        Returns:
            Vector
        """
        return Vector([a - b for a, b in zip(self.array, other.array)])

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
        return str([a for a in self.array])

    def __neg__(self):
        """override the negation operation (-obj)
        Returns:
            Vector: negated Vector
        """
        return Vector([a*-1 for a in self.array])

    def __eq__(self, other): 
        """override the comparation operation (==)
        Args:
            other (Vector): vector to compare
        Returns:
            bool: if both vectors are equal
        """
        for a, b in zip(self.array, other.array):
            if a != b:
                return False
        return True