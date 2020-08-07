import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import mUtils
import constants
from ..math_utils import rpd
from maya import cmds

def getNodesPosInRange(nodeList, timeRange=None):
    positionsDict = dict()
    if not timeRange:
        timeRange=getCurrentAnimRange()
    for node in nodeList:
        positionsDict[node] = getWorlPosInTimeRange(node, timeRange=timeRange)
    return positionsDict

def getCurrentAnimRange():
    return int(oma.MAnimControl.minTime().value), int(oma.MAnimControl.maxTime().value)

def getMatrixAttributeInTimeRange(node, attribute, timeRange=None):
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
    matrices = getMatrixAttributeInTimeRange(node, constants.WORDLMATRIX, timeRange=None)
    result = list()
    for matrix in matrices:
        result.append(list(matrix)[12:15])
    return result

def createAnimLayer(layerName, nodesToAdd=None):
    if not cmds.animLayer(layerName ,query=True, ex=True):
        layerName = cmds.animLayer(layerName)
    if nodesToAdd:
        cmds.select(nodesToAdd)
        cmds.animLayer(layerName, e=True, aso=True)
    cmds.animLayer(layerName, e=True, sel=True)

def getLayerAnimCurves(node, layerName):
    animCurves = set()
    for attr in cmds.listAttr(node, k=1):
        anim = cmds.animLayer(layerName, q=True,
                            findCurveForPlug='{}.{}'.format(node, attr))
        if anim:
            animCurves.update(anim)
    return list(animCurves)

def getCacheAttribute(animationCurve):
    cacheAttrName = '{}.{}'.format(animationCurve, constants.ANIMCACHEATTR)
    if not cmds.objExists(cacheAttrName):
        cmds.addAttr(animationCurve, longName=constants.ANIMCACHEATTR, dt='vectorArray')
    return cacheAttrName

def clearAnimCurve(animationCurve):
    fnAnimcurve = mUtils.getFn((animationCurve))
    [fnAnimcurve.remove(0) for a in range(int(fnAnimcurve.numKeys))]


def simplyfyAnimCurve(animationCurve, epsilon):
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
    cacheAttrName = getCacheAttribute(animationCurve)
    pointsArr = list()
    if cmds.objExists('{}.ktv[:]'.format(animationCurve)):
        points = cmds.getAttr('{}.ktv[:]'.format(animationCurve))
        pointsArr = [[a[0],a[1],0] for a in points]
    cmds.setAttr(cacheAttrName, len(pointsArr), *pointsArr, type='vectorArray')
    return pointsArr

