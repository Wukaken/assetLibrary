try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
from functools import partial


class ButtonView(basisView.BasisView):
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

        scaleFractor = self.dataCtrl.getDataVal('scaleFractor', 1)

        defWidSize = self.dataCtrl.getDataVal(
            'buttonWidgetSize', [176, 168])
        defPicSize = self.dataCtrl.getDataVal(
            'buttonPicmapSize', [160, 100])
        widSize = [defWidSize[0] * scaleFractor,
                   defWidSize[1] * scaleFractor]
        picSize = [defPicSize[0] * scaleFractor,
                   defPicSize[1] * scaleFractor]
        self.setFixedSize(widSize[0], widSize[1])
        self.picLabel.setFixedSize(picSize[0], picSize[1])

    def connectFunc(self):
        #self.funcCB.activated.connect(self.itemInnerFunc)
        return

    def initContent(self):
        currentDir = self.dataCtrl.getDataVal('currentDir')
        pic = self.dataCtrl.getDataVal('picFile')
        picFile = os.path.join(currentDir, pic).replace('\\', '/')

        self.picmap.load(pic)
        self.picLabel.setPixmap(self.picmap)
        self.picLabel.setScaledContents(1)

        for outInfoKey, label in self.labelWidInfo.items():
            mess = '%s: %s' % (outInfoKey, self.dataCtrl.getDataVal(outInfoKey))
            label.setText(mess)
        #self.pubType
        self.funcBtn.setText('Menu')
        self.funcBtn.setMenu(self.menu)
        #self.funcCB.addItems(funcKeys)

        self.setupFuncMenu()
        self.initTooltips()

    def setupFuncMenu(self):
        funcKeys = self.dataCtrl.getDataVal('funcKeys', [])
        funcInfo = self.dataCtrl.getDataVal('funcInfo')
        for funcKey in funcKeys:
            print funcKey
            self.menu.addAction(funcKey, self.printInfo)

    def initTooltips(self):
        for outInfoKey, label in self.labelWidInfo.items():
            mess = '%s: %s' % (outInfoKey, self.dataCtrl.getDataVal(outInfoKey))
            label.setToolTip(mess)

        tipKeys = self.dataCtrl.getDataVal('tipKeys')
        allMess = ''
        for tipKey in tipKeys:
            mess = '%s: %s\n' % (tipKey, self.dataCtrl.getDataVal(tipKey))
            allMess += mess
            
        self.picLabel.setToolTip(allMess)

    def printInfo(self):
        print 'diao'


            
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = ButtonView()
    v.do(ctrl)
    v.show()
    app.exec_()        
