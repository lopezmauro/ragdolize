# -*- coding: utf-8 -*-
"""Basic maya.api utils

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
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma

FNTYPES = [(om.MFn.kAnimCurve,oma.MFnAnimCurve),
           (om.MFn.kDagNode, om.MFnDagNode),
           om.MFn.kDependencyNode, om.MFnDagNode]

def getDependNode(node):
    """get maya api depend node object form a node name
    Args:
        node (str): node name
    Raises:
        ValueError: the provide argument is not a string ot MObject
    Returns:
        maya.api.MObject
    """
    if isinstance(node, om.MObject):
        return node
    if isinstance(node, basestring):
        sel = om.MSelectionList()
        sel.add(node)
        return sel.getDependNode(0)
    raise ValueError(node)


def getFn(node):
    """get maya api best MFn object form a node name, geting the best FN from
    FNTYPES constant
    Args:
        node (str): node name
    Raises:
        ValueError: the provide argument is not a string or MObject
    Returns:
        variable maya.api.MFtype
    """
    if isinstance(node, om.MFnBase):
        return node
    depNode = getDependNode(node)
    for fntype, fn in FNTYPES:
        if depNode.hasFn(fntype):
            return fn(depNode)
    raise ValueError(node)

def getIterSelection(nodeList):
    """create the iterSelection object form a list of node names

    Args:
        nodeList (list): list of node names

    Returns:
        maya.api.MItSelectionList
    """
    sel = om.MSelectionList()
    for node in nodeList:
        sel.add(node)
    return om.MItSelectionList(sel, om.MFn.kDagNode)

