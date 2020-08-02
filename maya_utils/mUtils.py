import math 
from maya.api import OpenMaya as om

def getFn(node):
    if isinstance(node, om.MFnDependencyNode):
        return node
    if isinstance(node, om.MObject):
        return om.MFnDependencyNode(node)
    if isinstance(node, basestring):
        sel = om.MSelectionList()
        sel.add(node)
        depNode = sel.getDependNode(0)
        if depNode.hasFn(om.MFn.kDagNode):
            return om.MFnDagNode(depNode)
        return om.MFnDependencyNode(depNode)
    raise ValueError(node)

def getIterSelection(nodeList):
    sel = om.MSelectionList()
    for node in nodeList:
        sel.add(node)
    return om.MItSelectionList(sel, om.MFn.kDagNode)

