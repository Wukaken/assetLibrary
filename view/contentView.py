try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
import buttonView
from functools import partial


class ContentView(basisView.BasisView):
    def __init__(self, parent=None):
        super(ContentView, self).__init__(parent)
        self.num = 5

    def buildElements(self):
        super(ContentView, self).buildElements()
        self.contLW = QtGui.QListWidget()
        self.detailLW = QtGui.QWidget()
        self.verionLW = QtGui.QListWidget()
        
        self.detailLabel = QtGui.QLabel('Detail:')
        self.historyLabel = QtGui.QLabel('History:')
        return
        
    def buildWidget(self):
        super(ContentView, self).buildWidget()

        self.mainLO.addWidget(self.mainFrame)

        self.frameLO.addWidget(self.titleLabel, 0, 0, 1, 2, self.centerAlign)
        self.frameLO.addWidget(self.contLW, 1, 0, 4, 1)
        self.frameLO.addWidget(self.detailLabel, 1, 1, self.centerAlign)
        self.frameLO.addWidget(self.detailLW, 2, 1)
        self.frameLO.addWidget(self.historyLabel, 3, 1, self.centerAlign)
        self.frameLO.addWidget(self.verionLW, 4, 1)

        self.contLW.setResizeMode(QtGui.QListView.Adjust)
        self.contLW.setMinimumWidth(250)
        self.contLW.setSpacing(1)
        self.contLW.setViewMode(QtGui.QListView.IconMode)
        self.contLW.setUniformItemSizes(True)

        self.detailLW.setFixedWidth(200)
        self.detailLW.setFixedHeight(200)
        self.verionLW.setFixedWidth(200)

        self.titleLabel.setText('Content')

    def connectFunc(self):
        self.contLW.itemClicked.connect(self.diao)

    def initContent(self):
        self.clearContentWidget()
        self.renewContentWidget()

    def clearContentWidget(self):
        self.contLW.clear()

    def renewContentWidget(self):
        defWidSize = self.dataCtrl.getDataVal(
            'buttonWidgetSize', [176, 168])
        for i in range(self.num):
            #'''
            #picmap = QtGui.QPixmap()
            #picmap.load('D:/a.png')
            #icon = QtGui.QIcon(picmap)
            #item = QtGui.QListWidgetItem(icon, 'idao')
            item = QtGui.QListWidgetItem()

            item.setSizeHint(QtCore.QSize(defWidSize[0] + 2, defWidSize[1] + 2))
            self.contLW.addItem(item)
            #'''
            v = buttonView.ButtonView()
            v.do(self.dataCtrl)
            #self.frameLO.addWidget(v)
            self.contLW.setItemWidget(item, v)
            #'''

        self.num -= 1

    def diao(self, item):
        print item

        popMenu = QtGui.QMenu()
        item.setMenu(popMenu)
        menu.addAction('asdfadf', self.printInfo)

    def printInfo(self):
        print 'getefdsq'

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ctrl = dc()
    v = ContentView()
    v.do(ctrl)
    v.show()
    app.exec_()        
            
