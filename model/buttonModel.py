import os
import basisModel


class ButtonModel(basisModel.BasisModel):
    def __init__(self, inJson, inData={}, presetJson=None):
        if presetJson is None:
            curDir = os.path.dirname(__file__)
            presetJson = os.path.join(curDir, 'buttonPreset.json').replace('\\', '/')

        super(ButtonModel, self).__init__(
            inJson, inData, presetJson=presetJson)
        self.storeKeys = []

    def normalizeData(self):
        metaData = self.getDataVal('metaData')
        fileType = metaData.get('fileType')
        typeFuncInfo = self.getDataVal('typeFuncInfo')
        funcInfo = typeFuncInfo.get(fileType, {})

        funcKeys = funcInfo.keys()
        initData = {'funcInfo': funcInfo,
                    'funcKeys': funcKeys,
                    'outInfoKeys': ['fileName', 'fileType'],
                    'tipsKeys': ['fileName', 'descStr',
                                 'fileType', 'fileType',
                                 'version'],
                    'defWidSize': [176, 168],
                    'defPicSize': [160, 100],
                    'scaleFractor': 1}
        self.completeData(initData)
