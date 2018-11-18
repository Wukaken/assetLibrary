try:
    from PySide2 import QtGui
    from PySide2 import QtCore
except:
    from PySide import QtGui
    from PySide import QtCore

import basisView
import buttonView
from control import buttonControl
from model import buttonModel
from functools import partial


class ContentView(basisView.BasisView):
    def __init__(self, parent=None):
        super(ContentView, self).__init__(parent)

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
        defWidSize = self.dataCtrl.getDataVal('buttonWidgetSize')
        scaleFractor = self.dataCtrl.getDataVal('buttonWidgetScaleFractor')
        itemSize = [defWidSize[0] * scaleFractor + 2,
                    defWidSize[1] * scaleFractor + 2]

        fileInfo = self.dataCtrl.getDataVal('contentFileInfo')
        files = fileInfo.keys()
        files.sort()
        for f in files:
            info = fileInfo[f]
            item = QtGui.QListWidgetItem()

            item.setSizeHint(QtCore.QSize(
                itemSize[0], itemSize[1]))
            self.contLW.addItem(item)
            self.buildUpItemView(info, item)

    def buildUpItemView(self, info, item):
        info['currentDir'] = self.dataCtrl.getDataVal('currentDir')
        btnV = buttonView.ButtonView()
        btnM = buttonModel.ButtonModel('', info)
        btnC = buttonControl.ButtonControl()

        btnC.do(btnV, btnM)
        btnV.do(btnC)
        self.contLW.setItemWidget(item, btnV)

    def diao(self):
        print 'idao'
