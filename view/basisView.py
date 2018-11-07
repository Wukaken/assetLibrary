try:
    from PySide2 import QtGui
except:
    from PySide import QtGui


class BasisView(QtGui.QDialog):
    def __init__(self, parent=None):
        super(BasisView, self).__init__(parent)
        self.dataCtrl = None

    def getMainWid(self):
        return self

    def do(self, dataCtrl):
        self.initCtrl(dataCtrl)

        self.buildElements()
        self.buildLayout()
        self.buildWidget()

        self.connectFunc()
        self.initContent()

    def initCtrl(self, dataCtrl):
        self.dataCtrl = dataCtrl

    def buildElement(self):
        return

    def buildLayout(self):
        self.mainLO = QtGui.QGridLayout()

    def buildWidget(self):
        return

    def connectFunc(self):
        return

    def initContent(self):
        return
