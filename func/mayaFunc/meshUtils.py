from maya import cmds
from maya import OpenMaya as om
import hashlib


def outputMeshNames():
    meshes = cmds.ls(type='mesh', ni=1)
    return meshes


def outputMeshTopoInfo():
    meshes = outputMeshNames()
    it = om.MItDag()
    topoInfo = {}
    while not it.isDone():
        mdag = om.MDagPath()
        it.getPath(mdag)
        dag = mdag.partialPathName()
        verNum = 0
        faceNum = 0
        topoMess = ''
        if dag in meshes:
            fnMesh = om.MFnMesh(mdag)
            verNum = fnMesh.numVertices()
            faceNum = fnMesh.numPolygons()
            if verNum and faceNum:
                ppVerCount = om.MIntArray()
                ppVerId = om.MIntArray()
                fnMesh.getVertices(ppVerCount, ppVerId)

                ppCount = list(ppVerCount)
                ppId = list(ppVerId)

                topoMess = '%s %s' % (verNum, faceNum)
                verIdNum = 0
                for i in range(faceNum):
                    topoMess += ' %s ' % i
                    verCount = ppCount[i]
                    newVerIdNum = verIdNum + verCount
                    verIds = ppId[verIdNum: newVerIdNum]
                    verIdNum = newVerIdNum
                    for verId in verIds:
                        topoMess += ' %s ' % verId

            topoId = hashlib.md5(topoMess).hexdigest()
            topoInfo[dag] = {'verNum': verNum,
                             'faceNum': faceNum,
                             'topoId': topoId}
        it.next()

    return topoInfo
