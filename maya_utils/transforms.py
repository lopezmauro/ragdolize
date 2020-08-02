import math
from maya.api import OpenMaya as om
from maya import cmds

def getAimRotation(drivenPos, targetPos, rotOrder='xyz',
                   aim=(1,0,0),
                   up=(0,1,0)):

    drivenPoint = om.MVector(drivenPos)
    targetPoint = om.MVector(targetPos)
    aimVector = om.MVector(aim)
    upVector = om.MVector(up)
    direction = (targetPoint-drivenPoint).normal()
    outAxis =  (direction ^ upVector).normal()
    ortoUp = (outAxis ^ direction).normal()
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

def getLocalTranslation(node, pos):
    mMatrix = om.MMatrix(cmds.getAttr('{}.pim'.format(node)))
    point = om.MPoint(pos)
    return om.MVector(point * mMatrix)

def getLocalRotation(node, rot):
    mMatrix = om.MMatrix(cmds.getAttr('{}.pm'.format(node)))
    trfMatrix = om.MTransformationMatrix()
    rotation = om.MVector([math.radians(a) for a in rot])
    euler = om.MEulerRotation(rotation)
    trfMatrix.rotateBy(euler, om.MSpace.kTransform)
    newMat = trfMatrix.asMatrix()
    newTrfMat = om.MTransformationMatrix(newMat * mMatrix)
    return [math.degrees(a) for a in newTrfMat.rotation()]