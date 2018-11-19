import re
import getpass
import os
import shutil
import basisControl


class ButtonControl(basisControl.BasisControl):
    def __init__(self):
        super(ButtonControl, self).__init__()

    def initFunc(self):
        return

    def checkOutFile(self):
        detailInnerDir = self.getDataVal('detailInnerDir')
        fileName = self.getDataVal('fileName')
        mat = '.v[\d]{3}.'
        toFileName = re.sub(mat, '.', fileName)

        toDir = os.path.dirname(detailInnerDir)
        oriJson = os.path.join(detailInnerDir, fileName)
        oriInfo = {}
        self.dataObj.inputDataFromFile(oriJson, oriInfo)
        oriMetaData = oriInfo['metaData']

        toJson = os.path.join(toDir, toFileName)
        toInfo = {}
        checkOutTest = 1
        outMess = ''
        self.dataObj.inputDataFromFile(toJson, toInfo)
        toMetaData = oriMetaData
        if oriMetaData['version'] == toMetaData['version']:
            checkOutTest = 0
            outMess = 'File: %s Check Same Version Out, do nothing' % fileName
        else:
            toInfo = oriInfo
            mainFileName = oriMetaData['fileName']
            picName = oriMetaData['picFile']
            mainFile = os.path.join(detailInnerDir, mainFileName)
            picFile = os.path.join(detailInnerDir, picName)

            toMainFileName = re.sub(mat, '.', mainFileName)
            toPicName = re.sub(mat, '.', picName)
            toMainFile = os.path.join(toDir, toMainFileName)
            toPicFile = os.path.join(toDir, toPicName)
            
            toInfo['metaData']['fileName'] = toFileName
            toInfo['metaData']['picFile'] = toPicName
            self.dataObj.outputDataToFile(toJson, toInfo)
            shutil.copy(mainFile, toMainFile)
            shutil.copy(picFile, toPicFile)

            outMess = 'File: %s has been checked out with %s by %s' % (toMainFile, mainFile, getpass.getuser())

        self.widget.emitCheckOutSignal(outMess, checkOutTest)
