import re
import getpass
import os
import shutil
import datetime
import basisControl
from func.basis import compareUtil
from func.basis import detailInfoUtil


class ButtonControl(basisControl.BasisControl):
    def __init__(self):
        super(ButtonControl, self).__init__()
        self.initFuncInfo()

    def initFuncInfo(self):
        self.funcInfo = {
            'checkOutFile': self.checkOutFile,
            'openMayaFileAs': self.openMayaFileAs,
            'compareDiffVersion': self.compareWithVersions,
            'compareDiffMain': self.compareWithMainFile,
            'compareDiffCurrentScene': self.compareWithCurrentScene
        }

    def getFunc(self, funcName):
        return self.funcInfo.get(funcName)

    def checkOutFile(self):
        oriJson = self.getDataVal('inputJson')
        
        currentDir = self.getDataVal('currentDir')
        metaData = self.getDataVal('metaData')
        fileName = metaData['fileName']
        jsonName = os.path.basename(oriJson)
        mat = '.v[\d]{3}.'
        toJsonName = re.sub(mat, '.', jsonName)

        toDir = os.path.dirname(currentDir)
        oriInfo = {}
        self.dataObj.inputDataFromFile(oriJson, oriInfo)
        oriMetaData = oriInfo['metaData']

        toJson = os.path.join(toDir, toJsonName).replace('\\', '/')
        toInfo = {}
        self.dataObj.inputDataFromFile(toJson, toInfo)
        toMetaData = toInfo['metaData']
        
        checkOutTest = 1
        outMess = ''
        subject = ''
        if oriMetaData['version'] == toMetaData['version']:
            checkOutTest = 0
            outMess = 'File: %s Check Same Version Out, do nothing' % fileName
            subject = 'File: %s Checkout Failed' % fileName
        else:
            toMetaData = oriMetaData

            toInfo = oriInfo
            mainFileName = oriMetaData['fileName']
            picName = oriMetaData['picFile']
            mainFile = os.path.join(currentDir, mainFileName).replace('\\', '/')
            picFile = os.path.join(currentDir, picName).replace('\\', '/')

            toMainFileName = re.sub(mat, '.', mainFileName)
            toPicName = re.sub(mat, '.', picName)
            toMainFile = os.path.join(toDir, toMainFileName).replace('\\', '/')
            toPicFile = os.path.join(toDir, toPicName).replace('\\', '/')
            
            toInfo['metaData']['fileName'] = toMainFileName
            toInfo['metaData']['picFile'] = toPicName
            self.dataObj.outputDataToFile(toJson, toInfo)

            shutil.copy(mainFile, toMainFile)
            shutil.copy(picFile, toPicFile)

            outMess = 'File: %s has been checked out with %s by %s in %s' % (toMainFile, mainFile, getpass.getuser(), datetime.datetime.now().strftime('%Y%m%d_%H%M'))
            subject = 'Asset: %s Checkout Success' % mainFileName

        self.widget.emitCheckOutSignal(
            outMess, subject, checkOutTest)

    def openMayaFileAs(self):
        from func.mayaFunc import mayaDataIO

        currentDir = self.getDataVal('currentDir')
        metaData = self.getDataVal('metaData')
        fileName = metaData['fileName']
        oriMa = os.path.join(currentDir, fileName).replace('\\', '/')

        mayaDataIO.openFileAs(oriMa)

    def compareWithVersions(self):
        self.widget.emitCompareDiffVersionSignal()

    def compareWithMainFile(self):
        self.widget.emitCompareDiffMainFileSignal()

    def compareWithCurrentScene(self):
        bJson = self.getDataVal('inputJson')
        bInfo = {}
        self.dataObj.inputDataFromFile(bJson, bInfo)

        bMetaData = bInfo['metaData']
        fileType = bMetaData['fileType']

        info = {'outputFileType': fileType,
                'mayaInit': self.getDataVal('mayaInit')}
        detailOutObj = detailInfoUtil.DetailInfoUtil(info)
        detailInfo = detailOutObj.do()
        aInfo = {'metaData': {'fileName': 'currentFile'},
                 'detailData': detailInfo}

        cmpUtil = compareUtil.CompareUtil(aInfo, bInfo)
        diffInfo = {}
        cmpUtil.doCompare(diffInfo)
        self.widget.emitCompareDiffCurrentFileSignal(diffInfo)
        return diffInfo
