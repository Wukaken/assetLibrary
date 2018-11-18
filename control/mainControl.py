import os
import basisControl


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
        for f in validContentFiles:
            info = {}
            self.dataObj.inputDataFromFile(f, info)
            metaData = info.get('metaData')
            if metaData:
                fileType = metaData.get('fileType')
                metaKey = metaData.get('metaKey')
                if metaKey == 'assetLibrary' and \
                   fileType in activeFileTypes:
                    contentFileInfo[f] = info

        updateInfo = {'contentFileInfo': contentFileInfo}
        self.setData(updateInfo)
