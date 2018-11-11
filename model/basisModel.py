import os
import json


class BasisModel(object):
    def __init__(self, inJson, inData={}):
        self.data = inData
        self.inJson = inJson
        if os.path.isfile(self.inJson):
            inJsonData = {}
            self.inputDataFromFile(self.inJson, inJsonData)
            self.completeData(inJsonData)

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
