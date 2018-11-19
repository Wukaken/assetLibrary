import os
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView


class ButtonView(basisView.BasisView):
    checkOutFileSignal = QtCore.Signal(str, int)
    
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
        funcKeys = self.dataCtrl.getDataVal('funcKeys', [])
        funcInfo = self.dataCtrl.getDataVal('funcInfo')
        for funcKey in funcKeys:
            func = funcInfo.get(funcKey)
            self.menu.addAction(funcKey, func)

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

    def emitCheckOutSignal(self, outMess, checkOutTest):
        self.checkOutFileSignal.emit(outMess, checkOutTest)
