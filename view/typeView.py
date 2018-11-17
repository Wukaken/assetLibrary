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
            'outInfoKeys': ['fileName', 'fileType'],
            'fileTypes': ['Maya Look Dev', 'Maya Rig']
        }
        
    def getDataVal(self, key, defVal=None):
        return self.data.get(key, defVal)

    def setData(self, updateInfo):
        self.data.update(updateInfo)
        
class TypeView(basisView.BasisView):
    def __init__(self, parent=None):
        super(TypeView, self).__init__(parent)
        self.labelWidInfo = {}

    def buildElements(self):
        super(TypeView, self).buildElements()
        self.typeLW = QtGui.QListWidget()
        self.chkOnBtn = QtGui.QPushButton('Check On All')
        self.chkOffBtn = QtGui.QPushButton('Check Off All')

    def buildWidget(self):
        self.mainLO.addWidget(self.titleLabel, 0, 0, 1, 2, self.centerAlign)
        self.mainLO.addWidget(self.typeLW, 1, 0, 1, 2)
        self.mainLO.addWidget(self.chkOnBtn, 2, 0)
        self.mainLO.addWidget(self.chkOffBtn, 2, 1)
        self.setLayout(self.mainLO)

    def connectFunc(self):
        #self.funcCB.activated.connect(self.itemInnerFunc)
        return

    def initContent(self):
        self.titleLabel.setText('File Type Filter')
        fileTypes = self.dataCtrl.getDataVal('fileTypes')
        for fileType in fileTypes:
            item = QtGui.QListWidgetItem()
            ftCb = QtGui.QCheckBox(fileType, parent=self)
            self.typeLW.addItem(item)
            self.typeLW.setItemWidget(item, ftCb)
            item.setToolTip('FileType: %s' % fileType)


            
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = TypeView()
    v.do(ctrl)
    v.show()
    app.exec_()        
