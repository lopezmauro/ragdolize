import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import mUtils
import constants

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