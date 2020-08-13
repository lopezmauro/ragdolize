import math
from maya.api import OpenMaya as om
from maya import cmds
import animation 
def getAimRotation(drivenPos, targetPos, rotOrder='xyz',
                   aim=(1,0,0),
                   up=(0,1,0), outAxis=(0,0,1)):

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
    selList = om.MSelectionList() # make a sel list # MSelectionList
    #selList.add(target) # add our node by name
    selList.add(node) # add our node by name
    #mDagPath = selList.getDagPath(0)
    mdpThis = selList.getDagPath(0)
    mpTarget=om.MPoint(target)

    mmMatrix = mdpThis.inclusiveMatrix();
    mmMatrixInverse = mmMatrix.inverse();
    #    // Express the target point in this node's object space:
    mpTargetInThisSpace=om.MPoint(mpTarget * mmMatrixInverse);
    #    // Assuming that the vector 1, 0, 0 defines the position of the front of this node,
    #    // get the quaternion that describes the rotation to make that vector point to mpTargetInThisSpace:
    mqToTarget=om.MQuaternion (om.MVector(myAimAxis).rotateTo(om.MVector(mpTargetInThisSpace)));
    #    // Apply that rotation to this node:
    mftThis=om.MFnTransform (mdpThis.transform());
    mftThis.rotateBy(mqToTarget, om.MSpace.kPreTransform);
    #    // Get the new inverse transformation matrix of this node
    mmMatrix = mdpThis.inclusiveMatrix();
    mmMatrixInverse = mmMatrix.inverse();
    #    // Get the world up vector.
    mvUp=om.MVector( myUpDir)
    #    // Express the world up vector in this node's object space.
    mpWorldUpInThisSpace=om.MPoint (mvUp * mmMatrixInverse);
    #    // Get the quaternion that describes the rotation to make the local up vector point to the world up vector:
    mqToWorldUp=om.MQuaternion (om.MVector(om.MVector(myUpAxis)).rotateTo(om.MVector(mpWorldUpInThisSpace)));
    #    // Get the x-axis rotation from the quaternion 
    merToWorldUp=om.MEulerRotation (mqToWorldUp.asEulerRotation());
    merToWorldUp.y = 0.0;
    merToWorldUp.z = 0.0;
    #    // Apply that rotation to this node:
    mftThis.rotateBy(merToWorldUp, om.MSpace.kPreTransform);



def getLocalTranslation(node, pos, frame):
    # for some reason DGContex wont update properlly so
    cmds.currentTime(frame) # force frame to refresh matrix value
    parent = cmds.listRelatives(node, p=1, f=1)
    matrix = om.MMatrix(cmds.xform(parent, q=1, ws=1, m=1))
    point = om.MPoint(pos)
    point = om.MVector(point * matrix.inverse())
    return point

def getLocalRotation(node, rot, frame):
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