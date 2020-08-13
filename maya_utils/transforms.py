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
from maya.api import OpenMaya as om
from maya import cmds

def aimNode(node,target, myAimAxis=[1,0,0], myUpAxis=[0,1,0], myUpDir=[0,0,1]):
    """rotate a transform to aim a target point
    Args:
        node (str): transform node name
        target (list): world space point expresed as [float, float, float]
        myAimAxis (list, optional): the axis that point to the target. Defaults to [1,0,0].
        myUpAxis (list, optional): the axis up to stabilize the rotation. Defaults to [0,1,0].
        myUpDir (list, optional): [description]. Defaults to [0,0,1].
    """    
    selList = om.MSelectionList()
    selList.add(node)
    mdpThis = selList.getDagPath(0)
    mpTarget=om.MPoint(target)

    mmMatrix = mdpThis.inclusiveMatrix();
    mmMatrixInverse = mmMatrix.inverse();
    mpTargetInThisSpace=om.MPoint(mpTarget * mmMatrixInverse);
    mqToTarget=om.MQuaternion (om.MVector(myAimAxis).rotateTo(om.MVector(mpTargetInThisSpace)));
    # Apply that rotation to this node:
    mftThis=om.MFnTransform (mdpThis.transform());
    mftThis.rotateBy(mqToTarget, om.MSpace.kPreTransform);
    
    mmMatrix = mdpThis.inclusiveMatrix();
    mmMatrixInverse = mmMatrix.inverse();
    mvUp=om.MVector(myUpDir)
    mpWorldUpInThisSpace=om.MPoint (mvUp * mmMatrixInverse);
    # Get the quaternion that describes the rotation to make the local up vector point to the world up vector:
    mqToWorldUp=om.MQuaternion (om.MVector(om.MVector(myUpAxis)).rotateTo(om.MVector(mpWorldUpInThisSpace)));
    merToWorldUp=om.MEulerRotation (mqToWorldUp.asEulerRotation());
    merToWorldUp.y = 0.0;
    merToWorldUp.z = 0.0;
    # Apply that rotation to this node:
    mftThis.rotateBy(merToWorldUp, om.MSpace.kPreTransform);


def getLocalTranslation(node, pos, frame):
    """the the local values to a note to reach a world position on specific frame
    Args:
        node (str): node name
        pos (list): world space point expresed as [float, float, float]
        frame (int): frame to get the node position

    Returns:
        list: node local space point expresed as [float, float, float]
    """    
    # for some reason DGContex wont update properlly so
    cmds.currentTime(frame) # force frame to refresh matrix value
    parent = cmds.listRelatives(node, p=1, f=1)
    matrix = om.MMatrix(cmds.xform(parent, q=1, ws=1, m=1))
    point = om.MPoint(pos)
    point = om.MVector(point * matrix.inverse())
    return point

def getLocalRotation(node, rot, frame):
    """the the local values to a note to reach a world rotation on specific frame
    Args:
        node (str): node name
        rot (list): world space roation expresed as [float, float, float]
        frame (int): frame to get the node position

    Returns:
        list: node local space rotation expresed as degrees [float, float, float]
    """   
    # for some reason DGContex wont update properlly so
    cmds.currentTime(frame) # force frame to refresh matrix value
    parent = cmds.listRelatives(node, p=1, f=1)
    matrix = om.MMatrix(cmds.xform(parent, q=1, ws=1, m=1))
    trfMatrix = om.MTransformationMatrix()
    rotation = om.MVector([math.radians(a) for a in rot])
    euler = om.MEulerRotation(rotation)
    trfMatrix.rotateBy(euler, om.MSpace.kTransform)
    newMat = trfMatrix.asMatrix()
    newTrfMat = om.MTransformationMatrix(newMat *  matrix.inverse())
    return [math.degrees(a) for a in newTrfMat.rotation()]