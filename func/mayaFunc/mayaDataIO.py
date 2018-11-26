import os
import shutil
from maya import cmds
from maya import mel
import tempfile


def getMayaFileType(mayaFile):
    if mayaFile.lower().endswith('.ma'):
        return 'mayaAscii'
    elif mayaFile.lower().endswith('.mb'):
        return 'mayaBinary'
    elif mayaFile.lower().endswith('.abc'):
        return 'Alembic'

    
def openMayaFile(mayaFile, pmtSpec=1, lnrSpec=0, loadDepth=''):
    fileType = getMayaFileType(mayaFile)
    mel.eval('$gUseScenePanelConfig = false')
    if lnrSpec == 1:
        loadDepth = 'none'
    
    if loadDepth:
        cmds.file(mayaFile, type=fileType, f=1, options='v=0',
                  lrd=loadDepth, prompt=pmtSpec, open=1, uc=0)
    else:
        cmds.file(mayaFile, type=fileType, f=1, options='v=0',
                  prompt=pmtSpec, open=1, uc=0)


def cleanMayaUI():
    '''cause maya UI slow down the transfer speed'''
    if not cmds.about(b = 1):
        panels = cmds.getPanel(vis=1)
        for panel in panels:
            if 'scriptEditorPanel' not in panel:
                win = "%sWindow" % panel
                if cmds.window(win, ex=1):
                    cmds.deleteUI(win)

                    
def saveMayaFile(mayaFile='', cleanUpUI=1):
    if not mayaFile:
        mayaFile = cmds.file(q=1, sn=1)
    if not mayaFile:
        mayaFile = tempfile.mktemp(suffix='.ma').replace('\\', '/')
    
    cmds.file(rn=mayaFile)
    fileType = getMayaFileType(mayaFile)
    if cleanMayaUI:
        cleanMayaUI()
        
    cmds.file(f=1, save=1, options="v=0", type=fileType, uc=0)
    return mayaFile


def openFileAs(oriMayaFile):
    curWorkspaces = cmds.workspace(q=1, lfw=1)
    curWorkspace = curWorkspaces[0]
    outDir = os.path.join(curWorkspace, 'scene').replace('\\', '/')
    if not os.path.isdir(outDir):
        os.makedirs(outDir)
        
    name = os.path.basename(oriMayaFile)
    temFile = os.path.join(curWorkspace, name).replace('\\', '/')
    parts = os.path.splitext(name)
    i = 0
    while os.path.isfile(temFile):
        curName = '%s_%s%s' % (parts[0], i, parts[1])
        temFile = os.path.join(curWorkspace, curName).replace('\\', '/')
        i += 1

    shutil.copy(oriMayaFile, temFile)
    openMayaFile(temFile)


def publishFile(temFile, outFile):
    outDir = os.path.dirname(outFile)
    addDir = os.path.join(outDir, 'innerFile')
    if not os.path.isdir(addDir):
        os.makedirs(addDir)

    nodeAttrInfo = {'file': 'ftn'}
    for node, attr in nodeAttrInfo.items():
        nodes = cmds.ls(type=node)
        for node in nodes:
            objAttr = '%s.%s' % (node, attr)
            val = cmds.getAttr(objAttr)
            toVal = os.path.join(addDir, os.path.basename(val)).replace('\\', '/')
            try:
                shutil.copy(val, toVal)
            except:
                pass

            cmds.setAttr(objAttr, toVal, type='string')

    saveMayaFile(temFile)
    shutil.copy(temFile, outFile)

