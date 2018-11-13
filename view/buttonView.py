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
            'picFile': '/Users/wujiajian/Desktop/pipeline-1.jpg',
            'fileName': 'a_sdfadsfefewfwfewecdwcwcwtex.ma',
            'descStr': 'i am a test, i am a test,i am a testi am a test,,i am a testi am a test',
            'funcKeys': ['', 'efew', 'ereip'],
            'funcInfo': {}
        }
        
    def getDataVal(self, key, defVal=None):
        return self.data.get(key, defVal)

    def setData(self, updateInfo):
        self.data.update(updateInfo)
        
class ButtonView(basisView.BasisView):
    def __init__(self, parent=None):
        super(ButtonView, self).__init__(parent)

    def buildElements(self):
        self.picLabel = QtGui.QLabel()
        self.descLabel = QtGui.QLabel()
        self.fnLabel = QtGui.QLabel()
        self.funcCB = QtGui.QComboBox()
        self.picmap = QtGui.QPixmap()

    def buildWidget(self):
        self.mainLO.addWidget(self.picLabel, 0, 0, 3, 3)
        self.mainLO.addWidget(self.descLabel, 3, 0, 2, 3)
        self.mainLO.addWidget(self.fnLabel, 6, 0, 1, 2)
        self.mainLO.addWidget(self.funcCB, 6, 2)

        self.setLayout(self.mainLO)
        self.setFixedSize(200, 220)

        self.picLabel.setFixedSize(160, 130)

    def connectFunc(self):
        self.funcCB.activated.connect(self.itemInnerFunc)

    def initContent(self):
        pic = self.dataCtrl.getDataVal('picFile')
        descStr = self.dataCtrl.getDataVal('descStr')
        fileName = self.dataCtrl.getDataVal('fileName')
        funcKeys = self.dataCtrl.getDataVal('funcKeys', [])

        self.picmap.load(pic)
        self.picLabel.setPixmap(self.picmap)
        self.picLabel.setScaledContents(1)
        self.descLabel.setText('Desc: %s' % descStr)
        self.fnLabel.setText('Name: %s' % fileName)
        self.funcCB.addItems(funcKeys)

    def itemInnerFunc(self, actId):
        funcInfo = self.dataCtrl.getDataVal('funcInfo')
        funcKeys = self.dataCtrl.getDataVal('funcKeys')
        funcKey = funcKeys[actId]
        func = funcInfo.get(funcKey)
        print funcKey
        if func:
            func()

            
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = ButtonView()
    v.do(ctrl)
    v.show()
    app.exec_()        
