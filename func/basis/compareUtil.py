class CompareUtil(object):
    def __init__(self, aInfo, bInfo):
        self.aInfo = aInfo
        self.bInfo = bInfo

    def doCompare(self, diffInfo={}):
        self.aFile = self.getFileName(self.aInfo)
        self.bFile = self.getFileName(self.bInfo)
        diffInfo[self.aFile] = {}
        diffInfo[self.bFile] = {}
        diffInfo['fileList'] = [self.aFile, self.bFile]
        self.genDiffDetailData(diffInfo)

    def getFileName(self, info):
        metaData = info.get('metaData', {})
        fileName = metaData.get('fileName', '')
        return fileName

    def genDiffDetailData(self, diffInfo={}):
        aDetailInfo = self.aInfo.get('detailData', {})
        bDetailInfo = self.bInfo.get('detailData', {})
        allKeys = list(set(aDetailInfo).union(bDetailInfo))

        for dataKey in allKeys:
            aVal = aDetailInfo.get(dataKey, [])
            bVal = bDetailInfo.get(dataKey, [])
            if dataKey in ['meshNameData', 'controlNameData']:
                self.genDiffList(aVal, bVal, dataKey, diffInfo)
            elif dataKey == 'meshTopoData':
                self.getDiffTopoData(aVal, bVal, dataKey, diffInfo)
            elif dataKey == 'shaderConnectData':
                self.getDiffShaderConnectData(aVal, bVal, dataKey, diffInfo)

    def genDiffList(self, aList, bList, dataKey, diffInfo):
        aRes = list(set(aList) - set(bList))
        if aRes:
            diffInfo[self.aFile][dataKey] = {'Exist Only': aRes}
        bRes = list(set(bList) - set(aList))
        if bRes:
            diffInfo[self.bFile][dataKey] = {'Exist Only': bRes}

    def getDiffTopoData(self, aTopoInfo, bTopoInfo, dataKey, diffInfo):
        allKeys = list(set(aTopoInfo).union(bTopoInfo))

        diffInfo[self.aFile][dataKey] = {'difference': {}}
        diffInfo[self.bFile][dataKey] = {'difference': {}}
        outTest = 0
        for key in allKeys:
            if key not in aTopoInfo or key not in bTopoInfo:
                continue

            aTopoData = aTopoInfo[key]
            bTopoData = bTopoInfo[key]
            aDiffInfo = {}
            bDiffInfo = {}
            diffTest = 0
            for topoKey in aTopoData:
                aTopoVal = aTopoData[topoKey]
                bTopoVal = bTopoData[topoKey]
                if not aTopoVal == bTopoVal:
                    diffTest = 1
                    outTest = 1
                    aDiffInfo[topoKey] = aTopoVal
                    bDiffInfo[topoKey] = bTopoVal

            if diffTest:
                diffInfo[self.aFile][dataKey]['difference'][key] = aDiffInfo
                diffInfo[self.bFile][dataKey]['difference'][key] = bDiffInfo

        if not outTest:
            diffInfo[self.aFile].pop(dataKey)
            diffInfo[self.bFile].pop(dataKey)

    def getDiffShaderConnectData(self, aConInfo, bConInfo, dataKey, diffInfo):
        allKeys = list(set(aConInfo) + set(bConInfo))

        diffInfo[self.aFile][dataKey] = {'exist only': {},
                                         'different': {}}
        diffInfo[self.bFile][dataKey] = {'exist only': {},
                                         'different': {}}
        aExistTest = 0
        bExistTest = 0
        aDiffTest = 0
        bDiffTest = 0
        for key in allKeys:
            aConData = aConInfo.get(key, {})
            bConData = bConInfo.get(key, {})
            if aConData and not bConData:
                diffInfo[self.aFile][dataKey]['exist only'][key] = aConData
                aExistTest = 1
            elif not aConData and bConData:
                diffInfo[self.bFile][dataKey]['exist only'][key] = bConData
                bExistTest = 1
            else:
                if set(aConData) == set(bConData):
                    continue
                else:
                    aOnly = list(set(aConData) - set(bConData))
                    bOnly = list(set(bConData) - set(aConData))
                    if aOnly:
                        diffInfo[self.aFile][dataKey]['different'][key] = aOnly
                        aDiffTest = 1
                    if bOnly:
                        diffInfo[self.bFile][dataKey]['different'][key] = bOnly
                        aDiffTest = 1

        if not aExistTest and not aDiffTest:
            diffInfo[self.aFile].pop(dataKey)
        elif not aExistTest:
            diffInfo[self.aFile][dataKey].pop('exist only')
        elif not aDiffTest:
            diffInfo[self.aFile][dataKey].pop('different')

        if not bExistTest and not bDiffTest:
            diffInfo[self.bFile].pop(dataKey)
        elif not bExistTest:
            diffInfo[self.bFile][dataKey].pop('exist only')
        elif not bDiffTest:
            diffInfo[self.bFile][dataKey].pop('different')
