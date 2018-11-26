import os
import re
import shutil
import datetime
import getpass
import basisControl
from func.mail import mailUtil
from func.basis import compareUtil
from func.basis import detailInfoUtil


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

    def validOutputCheck(self):
        currentDir = self.getDataVal('currentDir')
        outputFileName = self.getDataVal('outputFileName', '')
        outputFileType = self.getDataVal('outputFileType')
        fileTypes = self.getDataVal('fileTypes')
        rec = 0
        outMess = ''
        if outputFileType not in fileTypes:
            outMess += 'FileType: %s not in valid fileTypes:\n %s\n' % (
                outputFileType, ' '.join(fileTypes))
            rec = 1
        if not outputFileName:
            outMess += 'Output File Name is Empty\n'
            rec = 1
        if '.' not in outputFileName:
            outMess += 'Output File Name does not contain a suffix\n'
            rec = 1
        if not os.path.isdir(currentDir):
            outMess += 'Output Dir: %s is not a directary\n'
            rec = 1
            
        out = [rec, outMess]
        return out

    def doCheckInCompare(self):
        outputTemFile = self.getDataVal('outputTemFile')
        detailInfo = self.outputCurrentFileDetailInfo()
        updateInfo = {'outputTemFile': outputTemFile,
                      'outputDetailInfo': detailInfo}
        self.setData(updateInfo)

        aInfo = {'metaData': {'fileName': 'currentFile'},
                 'detailData': detailInfo}
        validContentFiles = self.getDataVal('validContentFiles', {})
        outputFileName = self.getDataVal('outputFileName', '')
        bInfo = {}
        for validFile in validContentFiles:
            info = {}
            self.dataObj.inputDataFromFile(validFile, info)
            metaData = info.get('metaData')
            if metaData:
                fileName = metaData.get('fileName')
                if fileName == outputFileName:
                    bInfo = info
                    break
        
        cmpUtil = compareUtil.CompareUtil(aInfo, bInfo)
        diffInfo = {}
        cmpUtil.doCompare(diffInfo)
        return diffInfo

    def checkInFile(self):
        self.resetDetailFileInfo()
        ver = self.getLatestVersion()
        self.outputFile(ver, 1)
        self.outputFile(ver, 0)
        self.getDetailVersionInfo()
        self.triggerCheckInMail(ver)

    def resetDetailFileInfo(self):
        outputFileType = self.getDataVal('outputFileType')
        outputFileName = self.getDataVal('outputFileName')
        updateInfo = {'detailFileName': outputFileName,
                      'detailFileType': outputFileType}
        self.setData(updateInfo)
        self.getDetailVersionInfo()

    def getLatestVersion(self):
        detailVersionInfo = self.getDataVal('detailVersionInfo', {})
        verMax = 0
        if detailVersionInfo:
            verFiles = detailVersionInfo.keys()
            verFiles.sort()
            latestFile = verFiles[-1]

            verInfo = detailVersionInfo[latestFile]
            curVer = verInfo['metaData']['version']
            verMax = int(curVer[1:])
            
        verMax += 1
        ver = 'v%03d' % verMax
        return ver

    def outputFile(self, ver, mainOutput):
        temFile = self.getDataVal('outputTemFile')
        temPic = self.getDataVal('outputTemPic')
        detailInfo = self.getDataVal('outputDetailInfo')
        outputFileName = self.getDataVal('outputFileName')
        fileParts = os.path.splitext(outputFileName)
        picParts = []
        if temPic:
            picParts = os.path.splitext(temPic)
        
        currentDir = ''
        verStr = ''
        if mainOutput:
            currentDir = self.getDataVal('currentDir')
            verStr = ''
        else:
            currentDir = self.getDataVal('detailInnerDir')
            verStr = '.%s' % ver

        outMainName = '%s%s%s' % (fileParts[0], verStr, fileParts[1])
        outJsonName = '%s%s.json' % (fileParts[0], verStr)
        outPicName = ''
        if temPic:
            outPicName = '%s%s%s' % (fileParts[0], verStr, picParts[1])

        outputFileType = self.getDataVal('outputFileType')
        outInfo = {
            'metaData': {
                'descStr': self.getDataVal('outputDescStr', ''),
                'fileName': outMainName,
                'fileType': outputFileType,
                'metaKey': 'assetLibrary',
                'picFile': outPicName,
                'version': ver
            },
            'detailData': detailInfo
        }
        
        outJson = os.path.join(currentDir, outJsonName).replace('\\', '/')
        self.dataObj.outputDataToFile(outJson, outInfo)
        if temPic:
            outPic = os.path.join(currentDir, outPicName).replace('\\', '/')
            shutil.copy(temPic, outPic)
        outMain = os.path.join(currentDir, outMainName).replace('\\', '/')
        self.outputMainFile(temFile, outMain, outputFileType)

    def outputMainFile(self, temFile, outFile, outputFileType):
        from func.mayaFunc import mayaDataIO
        mayaDataIO.publishFile(temFile, outFile)

    def takeCurrentAppScreenShot(self):
        mayaInit = self.getDataVal('mayaInit')
        outPic = ''
        if mayaInit:
            from func.mayaFunc import mayaScreenShot
            outPic = mayaScreenShot.screenShotCurrentPanel()

        return outPic

    def outputCurrentAppFile(self):
        mayaInit = self.getDataVal('mayaInit')
        outFile = ''
        if mayaInit:
            from func.mayaFunc import mayaDataIO
            outFile = mayaDataIO.saveMayaFile()

        return outFile

    def outputCurrentFileDetailInfo(self):
        info = {'outputFileType': self.getDataVal('outputFileType'),
                'mayaInit': self.getDataVal('mayaInit')}
        
        detailOutObj = detailInfoUtil.DetailInfoUtil(info)
        detailInfo = detailOutObj.do()
        return detailInfo

    def triggerCheckInMail(self, ver):
        outputFileType = self.getDataVal('outputFileType')
        outputFileName = self.getDataVal('outputFileName')
        currentDir = self.getDataVal('currentDir')

        outFile = os.path.join(currentDir, outputFileName).replace('\\', '/')
        outMess = 'File: %s, type: %s, version: %s has been check in by user: %s in %s' % (outFile, outputFileType, ver, getpass.getuser(), datetime.datetime.now().strftime('%Y%m%d_%H%M'))
        subject = 'Asset: %s Checkin Success' % outputFileName

        mailInfo = {'mess': outMess,
                    'subject': subject}
        updateInfo = {'checkInOutputInfo': mailInfo}
        self.setData(updateInfo)
        # self.triggerMail(mailInfo)

