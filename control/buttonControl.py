import re
import getpass
import os
import shutil
import basisControl


class ButtonControl(basisControl.BasisControl):
    def __init__(self):
        super(ButtonControl, self).__init__()
        self.initFuncInfo()

    def initFuncInfo(self):
        self.funcInfo = {
            'checkOutFile': self.checkOutFile,
            'openFileAs': self.openFileAs,
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
        if oriMetaData['version'] == toMetaData['version']:
            checkOutTest = 0
            outMess = 'File: %s Check Same Version Out, do nothing' % fileName
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

            outMess = 'File: %s has been checked out with %s by %s' % (toMainFile, mainFile, getpass.getuser())

        self.widget.emitCheckOutSignal(outMess, checkOutTest)

    def openFileAs(self):
        from func.maya import mayaDataIO

        currentDir = self.getDataVal('currentDir')
        fileName = self.getDataVal('fileName')
        oriMa = os.path.join(currentDir, fileName).replace('\\', '/')
        mayaDataIO.openFileAs(oriMa)

    def compareWithVersions(self):
        self.widget.emitCompareDiffVersionSignal()

    def compareWithMainFile(self):
        self.widget.emitCompareDiffMainFileSignal()

    def compareWithCurrentScene(self):
        from func.maya import mayaDataCompare
        
        currentDir = self.getDataVal('currentDir')
        fileName = self.getDataVal('fileName')
        bFile = os.path.join(currentDir, fileName).replace('\\', '/')
        mayaDataCompare.compareDiffCurrentScene(bFile)
