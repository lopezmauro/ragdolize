 #!/usr/bin/python
 # -*- coding: utf-8 -*-
 # -*- coding: utf-8 -*-
"""The Ramer–Douglas–Peucker algorithm, is an algorithm that recreate 
a curve composed of line segments to a similar curve with fewer points.

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
from math import sqrt


def distance(a, b):
    """get the distance between two 2D points

    Args:
        a (list): two value array
        b (list): two value array

    Returns:
        float: the distance between points
    """
    return  sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def point_line_distance(point, start, end):
    """shortest ditance between a point and a line

    Args:
        point (list): two value array defining a point in 2D space
        start (list): two value array defining the start of a line in 2DSpace
        end (list): two value array defining the end of a line in 2DSpace

    Returns:
        float: shortest distance
    """
    if (start == end):
        return distance(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) -
            (start[0] - point[0]) * (end[1] - start[1])
        )
        d = sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d

def simplify(points, epsilon):
    """Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    if epsilon <= 0:
        return points
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        results = simplify(points[:index+1], epsilon)[:-1] + simplify(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]

    return results