import os
from model import basisModel


class DetailInfoUtil(basisModel.BasisModel):
    def __init__(self, initData, detailPresetJson=None):
        super(DetailInfoUtil, self).__init__('', initData)

        if not detailPresetJson:
            curDir = os.path.dirname(__file__)
            detailPresetJson = os.path.join(curDir, 'detailPreset.json').replace('\\', '/')

        self.detailPresetInfo = {}
        self.inputDataFromFile(detailPresetJson, self.detailPresetInfo)
        self.funcInfo = {}
        self.initFuncInfo()

    def initFuncInfo(self):
        self.funcInfo = {
            'outputMeshNameInfo': {'conditions': ['mayaInit'],
                                   'func': self.outputMeshNameInfo,
                                   'outName': 'meshNameData'},
            'outputMeshTopoInfo': {'conditions': ['mayaInit'],
                                   'func': self.outputMeshTopoInfo,
                                   'outName': 'meshTopoData'},
            'outputShaderConInfo': {'conditions': ['mayaInit'],
                                    'func': self.outputShaderConInfo,
                                    'outName': 'shaderConnectData'},
            'outputCtrlNameInfo': {'conditions': ['mayaInit'],
                                   'func': self.outputCtrlNameInfo,
                                   'outName': 'controlNameData'}
        }

    def do(self):
        funcNames = self.getFileTypeDetailFuncs()
        detailInfo = {}
        for funcName in funcNames:
            curFuncInfo = self.funcInfo.get(funcName)
            if curFuncInfo:
                conditions = curFuncInfo['conditions']
                appTest = 1
                for condition in conditions:
                    if not self.getDataVal(condition):
                        appTest = 0
                        break

                if appTest:
                    outName = curFuncInfo['outName']
                    func = curFuncInfo['func']
                    curDetailInfo = func()
                    detailInfo[outName] = curDetailInfo

        return detailInfo

    def getFileTypeDetailFuncs(self):
        fileType = self.getDataVal('outputFileType')
        funcNames = self.detailPresetInfo.get(fileType, [])
        return funcNames

    def outputMeshNameInfo(self):
        from func.mayaFunc import meshUtils
        meshes = meshUtils.outputMeshNames()
        return meshes

    def outputMeshTopoInfo(self):
        from func.mayaFunc import meshUtils
        topoInfo = meshUtils.outputMeshTopoInfo()
        return topoInfo

    def outputShaderConInfo(self):
        from func.mayaFunc import shaderUtils
        shaderConInfo = shaderUtils.outputShaderConInfo()
        return shaderConInfo

    def outputCtrlNameInfo(self):
        from func.mayaFunc import rigUtils
        ctrlNames = rigUtils.outputCtrlNames()
        return ctrlNames
