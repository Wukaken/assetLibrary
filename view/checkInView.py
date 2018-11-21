try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import cmpView
from functools import partial


class ChkInView(basisView.BasisView):
    def __init__(self, parent=None):
        super(ChkInView, self).__init__(parent)

    def buildElements(self):
        super(ChkInView, self).buildElements()

        self.diffLabel = QtGui.QLabel('Compare Different:')
        self.cmpView = cmpView.CmpView()
        self.cmpView.do(self.dataCtrl)

        self.nextBtn = QtGui.QPushButton('Next')

        self.descLabel = QtGui.QLabel('Description:')
        self.picLabel = QtGui.QLabel()
        self.descTE = QtGui.QTextEdit()
        self.screenBtn = QtGui.QPushButton('Screen Shot')
        self.publishBtn = QtGui.QPushButton('Publish')

    def buildWidget(self):
        super(ChkInView, self).buildWidget()

        self.mainLO.addWidget(self.diffLabel, 0, 0, 1, 2, self.centerAlign)
        self.mainLO.addWidget(self.cmpView, 1, 0, 1, 2, self.centerAlign)
        self.mainLO.addWidget(self.nextBtn, 2, 1)

    def initContent(self):
        self.cmpView.initContent()

    def connectFunc(self):
        self.nextBtn.clicked.connect(self.renewWidget)
        self.screenBtn.clicked.connect(self.takeScreenShot)
        self.publishBtn.clicked.connect(self.publishFile)

    def renewWidget(self):
        self.diffLabel.hide()
        self.diffLabel.close()
        self.cmpView.hide()
        self.cmpView.close()
        self.nextBtn.hide()
        self.nextBtn.close()

        self.mainLO.addWidget(self.descLabel, 0, 0, 1, 2, self.centerAlign)
        self.mainLO.addWidget(self.picLabel, 1, 0)
        self.mainLO.addWidget(self.descTE, 1, 1)
        self.mainLO.addWidget(self.screenBtn, 2, 0)
        self.mainLO.addWidget(self.publishBtn, 2, 1)

    def takeScreenShot(self):
        return

    def publishFile(self):
        return
