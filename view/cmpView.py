try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
from functools import partial


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
        super(CmpView, self).buildWidget()

        self.mainLO.addWidget(self.mainFrame)
        
        self.frameLO.addWidget(self.titleLabel, 0, 0, self.centerAlign)
        self.frameLO.addWidget(self.splitter)

        self.splitter.addWidget(self.aWid)
        self.splitter.addWidget(self.bWid)

        self.aWid.setLayout(self.aLO)
        self.aLO.addWidget(self.aLabel, 0, 0, self.centerAlign)
        self.aLO.addWidget(self.aTe, 1, 0)
        self.aLO.setSpacing(3)
        self.aLO.setContentsMargins(3, 2, 3, 4)
        
        self.bWid.setLayout(self.bLO)
        self.bLO.addWidget(self.bLabel, 0, 0, self.centerAlign)
        self.bLO.addWidget(self.bTe, 1, 0)
        self.bLO.setSpacing(3)
        self.bLO.setContentsMargins(3, 2, 3, 4)

        self.frameLO.setRowStretch(0, 0)
        self.frameLO.setRowStretch(1, 1)

    def initContent(self):
        self.titleLabel.setText('Compare View')
        self.aLabel.setText('asdf')
        self.bLabel.setText('basdf')
        
