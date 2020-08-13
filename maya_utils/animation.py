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
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import mUtils
import constants
from ..math_utils import rpd
from maya import cmds

def getCurrentAnimRange():
    """get active animation range
    Returns:
        tuple: (int(startFrame), int(endFrame))
    """
    return int(oma.MAnimControl.minTime().value), int(oma.MAnimControl.maxTime().value)

def getMatrixAttributeInTimeRange(node, attribute, timeRange=None):
    """get matrix atributtes on a range of frames wir maya DGContext
    Args:
        node (str): node name
        attribute (str): attribute name like worldMatrix or parentInverseMatrix
        timeRange (tuple, optional): start and end frames, if si not defined
            it will get the current active animation range. Defaults to None.
    Returns:
        list: list of matrices
    """
    fn = mUtils.getFn(node)
    plug = fn.findPlug(attribute, 0)
    if plug.isArray:
        plug.evaluateNumElements()
        plug = plug.elementByPhysicalIndex(0)
    if not timeRange:
        timeRange=getCurrentAnimRange()
    result = list()
    for x in range(int(timeRange[0]), int(timeRange[1])):
        timeContext = om.MDGContext(om.MTime(x))
        matrixO = plug.asMObject(timeContext)
        fnMat = om.MFnMatrixData(matrixO)
        matrix =  fnMat.matrix()
        result.append(matrix)
    return result

def getWorlPosInTimeRange(node, timeRange=None):
    """get world position of a node in a range of time
    Args:
        node (str): node names
        timeRange (tuple(int, int), optional): start and end frame. if si not
            defined it will get the current active animation range. Defaults to None.
    Returns:
        list: [[float, float, float], [float, float, float], ...]
    """
    matrices = getMatrixAttributeInTimeRange(node, constants.WORDLMATRIX, timeRange=None)
    result = list()
    for matrix in matrices:
        result.append(list(matrix)[12:15])
    return result

def getNodesPosInRange(nodeList, timeRange=None):
    """get world position of a lit of nodes in a range of time
    Args:
        nodeList (list): list of node names
        timeRange (tuple(int, int), optional): start and end frame. if si not
            defined it will get the current active animation range. Defaults to None.
    Returns:
        dict: {'nodeName':[posFrame1, posFrame2, ...], ...}
    """
    positionsDict = dict()
    if not timeRange:
        timeRange=getCurrentAnimRange()
    for node in nodeList:
        positionsDict[node] = getWorlPosInTimeRange(node, timeRange=timeRange)
    return positionsDict

def createAnimLayer(layerName, nodesToAdd=None):
    """create a new animation layer is not exists and set it active
    Args:
        layerName (str): new layer name
        nodesToAdd (list, optional): list of node names to include on the layer. Defaults to None.
    """
    if not cmds.animLayer(layerName ,query=True, ex=True):
        layerName = cmds.animLayer(layerName)
    if nodesToAdd:
        cmds.select(nodesToAdd)
        cmds.animLayer(layerName, e=True, aso=True)
    cmds.animLayer(layerName, e=True, sel=True)

def getLayerAnimCurves(node, layerName):
    """get animation curves asociated to an animationlayer
    Args:
        node (str): name of an animated node
        layerName (str): name of a animation layer
    Returns:
        list: animation curves names
    """
    animCurves = set()
    for attr in cmds.listAttr(node, k=1):
        anim = cmds.animLayer(layerName, q=True,
                            findCurveForPlug='{}.{}'.format(node, attr))
        if anim:
            animCurves.update(anim)
    return list(animCurves)

def getCacheAttribute(animationCurve):
    """get the point cache attribute name of an animation curve.
    It will create the attribute if dont exists
    Args:
        animationCurve (str): name iof animation curve
    Returns:
        str: full name of the attribute (curveName.attributeName)
    """
    cacheAttrName = '{}.{}'.format(animationCurve, constants.ANIMCACHEATTR)
    if not cmds.objExists(cacheAttrName):
        cmds.addAttr(animationCurve, longName=constants.ANIMCACHEATTR, dt='vectorArray')
    return cacheAttrName

def clearAnimCurve(animationCurve):
    """remove all key of an animation curves
    Args:
        animationCurve (str): animation curve name
    """
    fnAnimcurve = mUtils.getFn((animationCurve))
    [fnAnimcurve.remove(0) for a in range(int(fnAnimcurve.numKeys))]


def simplyfyAnimCurve(animationCurve, epsilon):
    """remove keys of the animation curve but preserving the overal shape

    Args:
        animationCurve (str): name of the animation curve
        epsilon (float): how much preserve the original keys
    """
    points = list()
    cacheAttrName = getCacheAttribute(animationCurve)
    points = cmds.getAttr(cacheAttrName)
    if not points:
        points = cacheCurvePoints(animationCurve)
    if not points:
        return
    animPoints = [a[:-1] for a in points]
    newPoints = rpd.simplify(animPoints, epsilon)
    fnAnimcurve = mUtils.getFn(animationCurve)
    #clear keys
    clearAnimCurve(fnAnimcurve)
    conversionValue = 1.0
    if fnAnimcurve.animCurveType == oma.MFnAnimCurve.kAnimCurveTA:
        conversionValue = om.MAngle(1.0).asDegrees()
    for time, value in newPoints:
        fnAnimcurve.addKey(om.MTime(time), value/conversionValue)


def cacheCurvePoints(animationCurve):
    """save a cache of the animation keys on a curve attribute

    Args:
        animationCurve (str): name of the animation curve

    Returns:
        list: list of animation keys as vector [(time, value, 0), ...]
    """
    cacheAttrName = getCacheAttribute(animationCurve)
    pointsArr = list()
    if cmds.objExists('{}.ktv[:]'.format(animationCurve)):
        points = cmds.getAttr('{}.ktv[:]'.format(animationCurve))
        pointsArr = [[a[0],a[1],0] for a in points]
    cmds.setAttr(cacheAttrName, len(pointsArr), *pointsArr, type='vectorArray')
    return pointsArr

