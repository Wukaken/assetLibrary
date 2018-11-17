try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
from functools import partial

class dc(object):
    def __init__(self):
        self.data = {
            #'picFile': '/Users/wujiajian/Desktop/pipeline-1.jpg',
            'picFile': 'D:/a.png',
            'fileName': 'a_sdfadsfefewfwfewecdwcwcwtex.ma',
            'descStr': 'i am a test, i am a test,i am a testi am a test,,i am a testi am a test',
            'fileType': 'Maya Look File',
            'version': 'v001',
            'tipKeys': ['fileName', 'fileType', 'version', 'descStr'],
            'funcKeys': ['', 'efew', 'ereip'],
            'funcInfo': {},
            'outInfoKeys': ['fileName', 'fileType']
        }
        
    def getDataVal(self, key, defVal=None):
        return self.data.get(key, defVal)

    def setData(self, updateInfo):
        self.data.update(updateInfo)
        
class ButtonView(basisView.BasisView):
    def __init__(self, parent=None):
        super(ButtonView, self).__init__(parent)
        self.labelWidInfo = {}

    def buildElements(self):
        outInfoKeys = self.dataCtrl.getDataVal('outInfoKeys')
        self.mainFrame = QtGui.QFrame()

        self.picLabel = QtGui.QLabel()
        self.funcBtn = QtGui.QToolButton()
        self.picmap = QtGui.QPixmap()
        self.menu = QtGui.QMenu()

        for outInfoKey in outInfoKeys:
            label = QtGui.QLabel()
            self.labelWidInfo[outInfoKey] = label

        self.firLO = QtGui.QGridLayout()

    def buildWidget(self):
        self.firLO.addWidget(self.mainFrame, 0, 0)
        
        self.mainLO.addWidget(self.picLabel, 0, 0, 3, 3)
        i = 3
        outInfoKeys = self.dataCtrl.getDataVal('outInfoKeys')
        for outInfoKey in outInfoKeys:
            label = self.labelWidInfo[outInfoKey]
            self.mainLO.addWidget(label, i, 0, 1, 3)
            i += 1

        i -= 1
        self.mainLO.addWidget(self.funcBtn, i, 2)


        self.mainFrame.setLayout(self.mainLO)
        self.mainFrame.setFrameShape(QtGui.QFrame.Box)
        
        self.setLayout(self.firLO)
        scaleFractor = self.dataCtrl.getDataVal('scaleFractor', 1)
        widSize = [200, 220]
        picSize = [160, 130]
        self.setFixedSize(widSize[0] * scaleFractor, widSize[1] * scaleFractor)

        self.picLabel.setFixedSize(picSize[0] * scaleFractor, picSize[1] * scaleFractor)

    def connectFunc(self):
        #self.funcCB.activated.connect(self.itemInnerFunc)
        return

    def initContent(self):
        pic = self.dataCtrl.getDataVal('picFile')

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
