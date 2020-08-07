import math 
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma

FNTYPES = [(om.MFn.kAnimCurve,oma.MFnAnimCurve),
           (om.MFn.kDagNode, om.MFnDagNode),
           om.MFn.kDependencyNode, om.MFnDagNode]

def getDependNode(node):
    if isinstance(node, om.MObject):
        return node
    if isinstance(node, basestring):
        sel = om.MSelectionList()
        sel.add(node)
        return sel.getDependNode(0)
    raise ValueError(node)

def getFn(node):
    if isinstance(node, om.MFnBase):
        return node
    depNode = getDependNode(node)
    for fntype, fn in FNTYPES:
        if depNode.hasFn(fntype):
            return fn(depNode)
    raise ValueError(node)

def getIterSelection(nodeList):
    sel = om.MSelectionList()
    for node in nodeList:
        sel.add(node)
    return om.MItSelectionList(sel, om.MFn.kDagNode)

