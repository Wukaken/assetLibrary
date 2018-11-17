try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
from functools import partial
import buttonView

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
            'fileTypes': ['Maya Look File', 'Maya Rig'],
            'funcInfo': {},
            'outInfoKeys': ['fileName', 'fileType']
        }
        
    def getDataVal(self, key, defVal=None):
        return self.data.get(key, defVal)

    def setData(self, updateInfo):
        self.data.update(updateInfo)


class FuncView(basisView.BasisView):
    def __init__(self, parent=None):
        super(FuncView, self).__init__(parent)

    def buildElements(self):
        super(FuncView, self).buildElements()
        self.ftLabel = QtGui.QLabel('File Type:')
        self.ftCB = QtGui.QComboBox()

        self.fnLabel = QtGui.QLabel('File Name:')
        self.fnLE = QtGui.QLineEdit()
        self.autoFnBtn = QtGui.QPushButton('Config Name')

        self.mailLabel = QtGui.QLabel('Mail List:')
        self.mailTE = QtGui.QTextEdit()
        self.chkInBtn = QtGui.QPushButton('Check In')
        self.chkOutBtn = QtGui.QPushButton('Check Out')

    def buildWidget(self):
        self.mainLO.addWidget(self.titleLabel, 0, 0, 1, 3, self.centerAlign)
        
        self.mainLO.addWidget(self.ftLabel, 10, 0)
        self.mainLO.addWidget(self.ftCB, 10, 1, 1, 2)

        self.mainLO.addWidget(self.fnLabel, 20, 0)
        self.mainLO.addWidget(self.fnLE, 20, 1)
        self.mainLO.addWidget(self.autoFnBtn, 20, 2)

        self.mainLO.addWidget(self.mailLabel, 30, 0, 1, 2, self.centerAlign)
        self.mainLO.addWidget(self.mailTE, 31, 0, 3, 2)
        self.mainLO.addWidget(self.chkInBtn, 31, 2)
        self.mainLO.addWidget(self.chkOutBtn, 32, 2)

        self.mainLO.setRowStretch(33, 1)

        self.titleLabel.setText('Function')

        self.setLayout(self.mainLO)

    def connectFunc(self):
        return

    def initContent(self):
        fileTypes = self.dataCtrl.getDataVal('fileTypes')
        self.ftCB.addItems(fileTypes)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = FuncView()
    v.do(ctrl)
    v.show()
    app.exec_()        
            
