import os
import re
import basisControl
from func.mail import mailUtil
from func.basis import compareUtil


class MainControl(basisControl.BasisControl):
    def __init__(self):
        super(MainControl, self).__init__()

    def genDirValidContentInfo(self):
        self.genDirValidFiles()
        self.genFileContentInfo()

    def genDirValidFiles(self):
        currentDir = self.getDataVal('currentDir')

        tem = os.listdir(currentDir)
        validContentFiles = []
        for t in tem:
            full = os.path.join(currentDir, t).replace('\\', '/')
            if t.endswith('.json') and os.path.isfile(full):
                validContentFiles.append(full)

        updateInfo = {'validContentFiles': validContentFiles}
        self.setData(updateInfo)

    def genFileContentInfo(self):
        validContentFiles = self.getDataVal('validContentFiles')
        activeFileTypes = self.getDataVal('activeFileTypes')
        contentFileInfo = {}
        self.genContentInfo(
            validContentFiles, activeFileTypes, contentFileInfo)

        updateInfo = {'contentFileInfo': contentFileInfo}
        self.setData(updateInfo)

    def genContentInfo(self, files, validTypes, fileInfo):
        for f in files:
            info = {}
            self.dataObj.inputDataFromFile(f, info)
            metaData = info.get('metaData')
            if metaData:
                fileType = metaData.get('fileType')
                metaKey = metaData.get('metaKey')
                if metaKey == 'assetLibrary' and \
                   fileType in validTypes:
                    fileInfo[f] = info

    def getDetailVersionInfo(self):
        currentDir = self.getDataVal('currentDir')
        detailFileName = self.getDataVal('detailFileName')
        detailFileType = self.getDataVal('detailFileType')
        innerDir = os.path.join(currentDir, 'innerVersion').replace('\\', '/')

        tem = os.listdir(innerDir)
        header = '.'.join(detailFileName.split('.')[: -1])
        mat = '^%s.v[\d]{3}.json$' % header
        versionFiles = []
        for t in tem:
            if re.search(mat, t):
                full = os.path.join(innerDir, t).replace('\\', '/')
                versionFiles.append(full)

        detailVersionInfo = {}
        self.genContentInfo(
            versionFiles, [detailFileType], detailVersionInfo)

        updateInfo = {'detailVersionInfo': detailVersionInfo,
                      'detailInnerDir': innerDir}
        self.setData(updateInfo)

    def triggerMail(self, mailInfo):
        mailList = self.getDataVal('mailList')
        m = mailUtil.MailUtils()
        m.sendMail(mailList, mailInfo)

    def compareDiffFiles(self, aJson, bJson):
        aInfo = {}
        self.dataObj.inputDataFromFile(aJson, aInfo)
        bInfo = {}
        self.dataObj.inputDataFromFile(bJson, bInfo)
        cmpUtil = compareUtil.CompareUtil(aInfo, bInfo)
        diffInfo = {}
        cmpUtil.doCompare(diffInfo)
        return diffInfo

    def checkInFile(self):
        
        return

