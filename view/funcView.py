try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
import buttonView
from functools import partial


class FuncView(basisView.BasisView):
    def __init__(self, parent=None):
        super(FuncView, self).__init__(parent)

    def buildElements(self):
        super(FuncView, self).buildElements()
        self.ftLabel = QtGui.QLabel('File Type:')
        self.ftCB = QtGui.QComboBox()

        self.fnLabel = QtGui.QLabel('File Name:')
        self.fnLE = QtGui.QLineEdit()
        self.autoFnBtn = QtGui.QPushButton('Config File Name')

        self.mailLabel = QtGui.QLabel('Mail List:')
        self.mailTE = QtGui.QTextEdit()
        self.chkInBtn = QtGui.QPushButton('Check In')

    def buildWidget(self):
        super(FuncView, self).buildWidget()
        self.mainLO.addWidget(self.mainFrame)
        
        self.frameLO.addWidget(self.titleLabel, 0, 0, 1, 2, self.centerAlign)
        
        self.frameLO.addWidget(self.ftLabel, 1, 0)
        self.frameLO.addWidget(self.ftCB, 1, 1, 1)

        self.frameLO.addWidget(self.fnLabel, 2, 0)
        self.frameLO.addWidget(self.fnLE, 2, 1)

        self.frameLO.addWidget(self.chkInBtn, 3, 0)
        self.frameLO.addWidget(self.autoFnBtn, 3, 1)

        self.frameLO.addWidget(self.mailLabel, 4, 0, self.centerAlign)

        self.frameLO.addWidget(self.mailTE, 5, 0, 3, 2)

        self.frameLO.setRowStretch(4, 1)
        self.titleLabel.setText('Function')
        # self.setFixedWidth(250)

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
            
