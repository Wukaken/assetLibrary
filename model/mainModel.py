import os
import basisModel


class MainModel(basisModel.BasisModel):
    def __init__(self, inJson, inData={}, presetJson=None):
        super(MainModel, self).__init__(inJson, inData=inData, presetJson=presetJson)
        self.storeKeys = [
            'projectRoot', 'currentDir', 'activeFileTypes',
            'fileType', 'mailList']
        self.generalKeys = ['mayaInit']

    def normalizeData(self):
        userDir = os.path.expanduser('~')
        currentDir = self.getDataVal('currentDir', userDir)
        initData = {
            'projectRoot': userDir,
            'currentDir': userDir,
            'currentDirs': [currentDir],
            'currentDirId': 0,

            'fileTypes': ['Maya Model File', 'Maya Look File', 'Maya Rig File'],
            'tipKeys': ['fileName', 'fileType', 'version', 'descStr'],
            'outInfoKeys': ['fileName', 'descStr'],
            'buttonWidgetSize': [176, 168],
            'buttonPicmapSize': [160, 100],
            'buttonWidgetScaleFractor': 1
        }
        self.completeData(initData)

        activeFileTypes = self.getDataVal('activeFileTypes', [])
        fileTypes = self.getDataVal('fileTypes')
        if not activeFileTypes:
            activeFileTypes = fileTypes[:]
        else:
            rmIds = []
            for i, fileType in enumerate(activeFileTypes):
                if fileType not in fileTypes:
                    rmIds.insert(0, i)

            for rmId in rmIds:
                activeFileTypes.pop(rmId)

        updateInfo = {'activeFileTypes': activeFileTypes}
        self.setDataVal(updateInfo)
