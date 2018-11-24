import os
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView


class ButtonView(basisView.BasisView):
    checkOutFileSignal = QtCore.Signal(str, str, int)
    compareDiffVersionsSignal = QtCore.Signal()
    compareMainFileSignal = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(ButtonView, self).__init__(parent)
        self.labelWidInfo = {}

    def buildElements(self):
        super(ButtonView, self).buildElements()
        
        outInfoKeys = self.dataCtrl.getDataVal('outInfoKeys')
        self.picLabel = QtGui.QLabel()
        self.funcBtn = QtGui.QToolButton()
        self.picmap = QtGui.QPixmap()
        self.menu = QtGui.QMenu()

        for outInfoKey in outInfoKeys:
            label = QtGui.QLabel()
            self.labelWidInfo[outInfoKey] = label

    def buildWidget(self):
        super(ButtonView, self).buildWidget()
        
        self.mainLO.addWidget(self.mainFrame)

        self.frameLO.addWidget(self.picLabel, 0, 0, 3, 3)
        i = 3
        outInfoKeys = self.dataCtrl.getDataVal('outInfoKeys')
        for outInfoKey in outInfoKeys:
            label = self.labelWidInfo[outInfoKey]
            self.frameLO.addWidget(label, i, 0, 1, 3)
            i += 1

        i -= 1
        self.frameLO.addWidget(self.funcBtn, i, 2)

        scaleFractor = self.dataCtrl.getDataVal('scaleFractor')
        defWidSize = self.dataCtrl.getDataVal(
            'defWidSize')
        defPicSize = self.dataCtrl.getDataVal(
            'defPicSize')
        widSize = [defWidSize[0] * scaleFractor,
                   defWidSize[1] * scaleFractor]
        picSize = [defPicSize[0] * scaleFractor,
                   defPicSize[1] * scaleFractor]
        self.setFixedSize(widSize[0], widSize[1])
        self.picLabel.setFixedSize(picSize[0], picSize[1])

    def connectFunc(self):
        # self.funcCB.activated.connect(self.itemInnerFunc)
        return

    def initContent(self):
        currentDir = self.dataCtrl.getDataVal('currentDir')
        metaData = self.dataCtrl.getDataVal('metaData')
        pic = metaData.get('picFile', '')
        picFile = os.path.join(currentDir, pic).replace('\\', '/')

        self.picmap.load(picFile)
        self.picLabel.setPixmap(self.picmap)
        self.picLabel.setScaledContents(1)

        for outInfoKey, label in self.labelWidInfo.items():
            val = metaData.get(outInfoKey, '')
            mess = '%s: %s' % (outInfoKey, val)
            label.setText(mess)

        self.funcBtn.setText('Menu')
        self.funcBtn.setMenu(self.menu)

        self.setupFuncMenu()
        self.initTooltips()

    def setupFuncMenu(self):
        funcInfo = self.dataCtrl.getDataVal('funcInfo')
        allDesc = ''
        for funcKey, info in funcInfo.items():
            conditions = info['conditions']
            appTest = 1
            for condition in conditions:
                if not self.dataCtrl.getDataVal(condition):
                    appTest = 0
                    break

            if appTest:
                validTypes = info['validFileTypes']
                fileType = self.dataCtrl.getDataVal('fileType')
                if validTypes and fileType not in validTypes:
                    appTest = 0

            if appTest:
                funcName = info['func']
                func = self.dataCtrl.getFunc(funcName)
                if func:
                    desc = info['desc']
                    allDesc += '%s: %s\n' % (funcKey, desc)
                    self.menu.addAction(funcKey, func)

        self.menu.setToolTip(allDesc)

    def initTooltips(self):
        metaData = self.dataCtrl.getDataVal('metaData')
        for outInfoKey, label in self.labelWidInfo.items():
            val = metaData.get(outInfoKey)
            mess = '%s: %s' % (outInfoKey, val)
            label.setToolTip(mess)

        tipsKeys = self.dataCtrl.getDataVal('tipsKeys')
        allMess = ''
        for tipsKey in tipsKeys:
            val = metaData.get(tipsKey)
            mess = '%s: %s\n' % (tipsKey, val)
            allMess += mess
            
        self.picLabel.setToolTip(allMess)

    def emitCheckOutSignal(self, mess, subject, checkOutTest):
        self.checkOutFileSignal.emit(mess, subject, checkOutTest)

    def emitCompareDiffVersionSignal(self):
        self.compareDiffVersionsSignal.emit()

    def emitCompareDiffMainFileSignal(self):
        self.compareMainFileSignal.emit()

