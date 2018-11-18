import os
import json


class BasisModel(object):
    def __init__(self, inJson, inData={}, presetJson=None):
        self.storeKeys = ['projectRoot', 'currentDir', 'activeFileTypes']
        self.data = inData
        self.inJson = inJson
        self.presetJson = presetJson
        for curJson in [inJson, presetJson]:
            if curJson and os.path.isfile(curJson):
                inJsonData = {}
                self.inputDataFromFile(curJson, inJsonData)
                self.completeData(inJsonData)

        self.normalizeData()

    def normalizeData(self):
        userDir = os.path.expanduser('~')
        currentDir = self.getDataVal('currentDir', userDir)
        initData = {'projectRoot': userDir,
                    'currentDir': userDir,
                    'currentDirs': [currentDir],
                    'currentDirId': 0,

                    'fileTypes': ['Maya Look File', 'Maya Rig File'],
                    'tipKeys': ['fileName', 'fileType', 'version', 'descStr'],
                    'outInfoKeys': ['fileName', 'descStr']}
        self.completeData(initData)

        activeFileTypes = self.getDataVal('activeFileTypes', [])
        fileTypes = self.getDataVal('fileTypes')
        if not activeFileTypes:
            activeFileTypes = fileTypes[:]
        else:
            for activeFileType in activeFileTypes:
                if activeFileType in fileTypes:
                    activeFileTypes.append(activeFileType)

        updateInfo = {'activeFileTypes': activeFileTypes}
        self.setDataVal(updateInfo)

    def completeData(self, inData):
        for key, val in inData.items():
            if key not in self.data:
                self.data[key] = val

    def setDataVal(self, updateData):
        self.data.update(updateData)

    def getDataVal(self, specKey, defVal=None):
        rec = self.data.get(specKey)
        if rec is None:
            rec = defVal

        return rec

    def inputDataFromFile(self, inJson, inData):
        rId = open(inJson, 'rb')
        curData = json.load(rId)
        rId.close()

        inData.update(curData)

    def outputDataToFile(self, outJson, outData):
        wId = open(outJson, 'wb')
        json.dump(outData, wId, sort_keys=1, indent=2)
        wId.close()

    def getSpecDatas(self, keys):
        info = {}
        for key in keys:
            info[key] = self.getDataVal(key)

        return info

    def genStoreData(self):
        storeData = self.getSpecDatas(self.storeKeys)
        return storeData

    def outPresetFile(self, outJson=None):
        if not outJson and self.presetJson:
            outJson = self.presetJson

        if not outJson:
            return

        outDir = os.path.dirname(outJson)
        if not os.path.isdir(outDir):
            os.makedirs(outDir)

        storeData = self.genStoreData()
        self.outputDataToFile(outJson, storeData)
