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
import animation 
def getAimRotation(drivenPos, targetPos, rotOrder='xyz',
                   aim=(1,0,0),
                   up=(0,1,0), outAxis=(0,0,1)):
    """[summary]

    Args:
        drivenPos ([type]): [description]
        targetPos ([type]): [description]
        rotOrder (str, optional): [description]. Defaults to 'xyz'.
        aim (tuple, optional): [description]. Defaults to (1,0,0).
        up (tuple, optional): [description]. Defaults to (0,1,0).
        outAxis (tuple, optional): [description]. Defaults to (0,0,1).

    Returns:
        [type]: [description]
    """
    drivenPoint = om.MVector(drivenPos)
    targetPoint = om.MVector(targetPos)
    aimVector = om.MVector(aim)
    upVector = om.MVector(up)
    outVector = om.MVector(outAxis)
    direction = (targetPoint-drivenPoint).normal()
    #outVector1 =  (direction ^ upVector).normal()
    #if outVector*outVector1>=-1:
    #    outVector1 = (upVector ^ direction).normal()
    ortoUp = (outVector ^ direction).normal()
    quaternion = om.MQuaternion(aimVector, direction)
    upRotated = upVector.rotateBy(quaternion)
    angle = math.acos(round(upRotated*ortoUp,2))
    quatAim = om.MQuaternion(angle, direction)
    #check if is the shortest path
    if not ortoUp.isEquivalent(upRotated.rotateBy(quatAim), 1.0e-4):
        #if not rotate it 360
        angle = (2*math.pi) - angle
        quatAim = om.MQuaternion(angle, direction)
    quaternion *= quatAim
    euler = quaternion.asEulerRotation()
    if isinstance(rotOrder, str) and hasattr(om.MTransformationMatrix,'k{}'.format(rotOrder.upper())):
        rotOrder = getattr(om.MEulerRotation,'k{}'.format(rotOrder.upper()))
    if isinstance(rotOrder, int):
        euler.reorderIt(rotOrder)
    return [math.degrees(a) for a in euler.asVector()]

def aimNode(node,target, myAimAxis=[1,0,0], myUpAxis=[0,1,0], myUpDir=[0,0,1]):
    """[summary]

    Args:
        node ([type]): [description]
        target ([type]): [description]
        myAimAxis (list, optional): [description]. Defaults to [1,0,0].
        myUpAxis (list, optional): [description]. Defaults to [0,1,0].
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
    mvUp=om.MVector( myUpDir)
    mpWorldUpInThisSpace=om.MPoint (mvUp * mmMatrixInverse);
    # Get the quaternion that describes the rotation to make the local up vector point to the world up vector:
    mqToWorldUp=om.MQuaternion (om.MVector(om.MVector(myUpAxis)).rotateTo(om.MVector(mpWorldUpInThisSpace)));
    merToWorldUp=om.MEulerRotation (mqToWorldUp.asEulerRotation());
    merToWorldUp.y = 0.0;
    merToWorldUp.z = 0.0;
    # Apply that rotation to this node:
    mftThis.rotateBy(merToWorldUp, om.MSpace.kPreTransform);



def getLocalTranslation(node, pos, frame):
    """[summary]

    Args:
        node ([type]): [description]
        pos ([type]): [description]
        frame ([type]): [description]

    Returns:
        [type]: [description]
    """    
    # for some reason DGContex wont update properlly so
    cmds.currentTime(frame) # force frame to refresh matrix value
    parent = cmds.listRelatives(node, p=1, f=1)
    matrix = om.MMatrix(cmds.xform(parent, q=1, ws=1, m=1))
    point = om.MPoint(pos)
    point = om.MVector(point * matrix.inverse())
    return point

def getLocalRotation(node, rot, frame):
    """[summary]

    Args:
        node ([type]): [description]
        rot ([type]): [description]
        frame ([type]): [description]

    Returns:
        [type]: [description]
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