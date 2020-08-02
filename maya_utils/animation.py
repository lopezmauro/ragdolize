import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import mUtils
import constants

def getNodesWorldMatrixInRange(nodeList, timeRange=None):
    positionsDict = dict()
    if not timeRange:
        timeRange=getCurrentAnimRange()
    for node in nodeList:
        positionsDict[node] = getMatrixInTimeRange(node, timeRange=timeRange)
    return positionsDict

def getCurrentAnimRange():
    return int(oma.MAnimControl.minTime().value), int(oma.MAnimControl.maxTime().value)

def getMatrixInTimeRange(node, timeRange=None):
    fn = mUtils.getFn(node)
    plugArray = fn.findPlug(constants.WORDLMATRIX, 0)
    plugArray.evaluateNumElements()
    plug = plugArray.elementByPhysicalIndex(0)
    if not timeRange:
        timeRange=getCurrentAnimRange()
    result = list()
    for x in range(*timeRange):
        timeContext = om.MDGContext(om.MTime(x))
        matrixO = plug.asMObject(timeContext)
        fnMat = om.MFnMatrixData(matrixO)
        matrix =  fnMat.matrix()
        result.append(list(matrix)[12:15])
    return result