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

class CmpView(basisView.BasisView):
    def __init__(self, parent=None):
        super(CmpView, self).__init__(parent)

    def buildElements(self):
        super(CmpView, self).buildElements()

        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.aWid = QtGui.QWidget()
        self.aLabel = QtGui.QLabel()
        self.aTe = QtGui.QTextEdit()
        self.aLO =QtGui.QGridLayout()
        self.bWid = QtGui.QWidget()
        self.bLabel = QtGui.QLabel()
        self.bTe = QtGui.QTextEdit()
        self.bLO =QtGui.QGridLayout()

    def buildWidget(self):
        self.mainLO.addWidget(self.titleLabel, 0, 0, self.centerAlign)
        self.mainLO.addWidget(self.splitter)

        self.splitter.addWidget(self.aWid)
        self.splitter.addWidget(self.bWid)

        self.aWid.setLayout(self.aLO)
        self.aLO.addWidget(self.aLabel, 0, 0, self.centerAlign)
        self.aLO.addWidget(self.aTe, 1, 0)
        
        self.bWid.setLayout(self.bLO)
        self.bLO.addWidget(self.bLabel, 0, 0, self.centerAlign)
        self.bLO.addWidget(self.bTe, 1, 0)

        self.setLayout(self.mainLO)

        self.mainLO.setRowStretch(0, 0)

    def initContent(self):
        self.titleLabel.setText('Compare View')
        self.aLabel.setText('asdf')
        self.bLabel.setText('basdf')
        
    
if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = CmpView()
    v.do(ctrl)
    v.show()
    app.exec_()        
