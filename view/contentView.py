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
        self.detailW = QtGui.QWidget()
        self.versionLW = QtGui.QListWidget()
        
        self.detailLabel = QtGui.QLabel('Detail:')
        self.historyLabel = QtGui.QLabel('History:')
        return
        
    def buildWidget(self):
        super(ContentView, self).buildWidget()

        self.mainLO.addWidget(self.mainFrame)

        self.frameLO.addWidget(self.titleLabel, 0, 0, 1, 2, self.centerAlign)
        self.frameLO.addWidget(self.contLW, 1, 0, 4, 1)
        self.frameLO.addWidget(self.detailLabel, 1, 1, self.centerAlign)
        self.frameLO.addWidget(self.detailW, 2, 1)
        self.frameLO.addWidget(self.historyLabel, 3, 1, self.centerAlign)
        self.frameLO.addWidget(self.versionLW, 4, 1)

        self.contLW.setResizeMode(QtGui.QListView.Adjust)
        self.contLW.setMinimumWidth(250)
        self.contLW.setSpacing(1)
        self.contLW.setViewMode(QtGui.QListView.IconMode)
        self.contLW.setUniformItemSizes(True)

        self.detailW.setFixedWidth(200)
        self.detailW.setFixedHeight(200)

        self.versionLW.setResizeMode(QtGui.QListView.Adjust)
        self.versionLW.setSpacing(1)
        self.versionLW.setUniformItemSizes(True)
        self.versionLW.setFixedWidth(200)
        self.versionLW.setSelectionMode(
            QtGui.QListWidget.SelectionMode.MultiSelection)

        self.titleLabel.setText('Content')

    def connectFunc(self):
        self.contLW.itemClicked.connect(self.showItemDetails)
        self.versionLW.itemClicked.connect(self.renewVersionSelection)

    def initContent(self):
        self.clearContentWidget()
        self.renewContentWidget(self.contLW, 'contentFileInfo',
                                self.buildUpContItemView,
                                reverse=0)

    def clearContentWidget(self):
        self.contLW.clear()

    def renewContentWidget(self, listWid, contKey,
                           buildItemFunc, outWidth=None,
                           reverse=0):
        defWidSize = self.dataCtrl.getDataVal('buttonWidgetSize')
        scaleFractor = self.dataCtrl.getDataVal('buttonWidgetScaleFractor')
        itemSize = [defWidSize[0] * scaleFractor + 2,
                    defWidSize[1] * scaleFractor + 2]
        if outWidth is not None:
            outScale = 1.0 * outWidth / itemSize[0]
            itemSize = [itemSize[0] * outScale,
                        itemSize[1] * outScale]

        fileInfo = self.dataCtrl.getDataVal(contKey)
        files = fileInfo.keys()
        files.sort(reverse=reverse)
        for f in files:
            info = fileInfo[f]
            item = QtGui.QListWidgetItem()

            item.setSizeHint(QtCore.QSize(
                itemSize[0], itemSize[1]))
            listWid.addItem(item)
            buildItemFunc(info, item, listWid)

    def buildUpContItemView(self, info, item, listWid):
        info['currentDir'] = self.dataCtrl.getDataVal('currentDir')
        btnV = buttonView.ButtonView()
        btnM = buttonModel.ButtonModel('', info)
        btnC = buttonControl.ButtonControl()

        btnC.do(btnV, btnM)
        btnV.do(btnC)
        listWid.setItemWidget(item, btnV)

    def showItemDetails(self, item):
        self.renewDetailVersionInfo(item)
        self.clearDetailWidget()
        self.renewDetailWidget(item)
        self.clearHistoryWidget()
        self.renewHistoryWidget()

    def renewDetailVersionInfo(self, item):
        oriBtnV = self.contLW.itemWidget(item)
        oriBtnM = oriBtnV.dataCtrl.dataObj

        metaData = oriBtnM.getDataVal('metaData')
        fileName = metaData.get('fileName')
        fileType = metaData.get('fileType')
        updateInfo = {'detailFileName': fileName,
                      'detailFileType': fileType,
                      'versionSelIds': []}
        self.dataCtrl.setData(updateInfo)
        self.dataCtrl.getDetailVersionInfo()
        
    def clearDetailWidget(self):
        if self.detailW:
            self.detailW.hide()
            self.detailW.close()
            self.detailW = None

    def renewDetailWidget(self, item):
        oriBtnV = self.contLW.itemWidget(item)
        oriBtnM = oriBtnV.dataCtrl.dataObj

        info = {}
        info.update(oriBtnM.data)
        info['scaleFractor'] = 1.15
        info['outInfoKeys'] = info['tipsKeys']
        btnV = buttonView.ButtonView()
        btnM = buttonModel.ButtonModel('', info)
        btnC = buttonControl.ButtonControl()

        btnC.do(btnV, btnM)
        btnV.do(btnC)
        self.detailW = btnV
        self.detailW.setFixedWidth(200)
        self.detailW.setFixedHeight(200)
        self.frameLO.addWidget(self.detailW, 2, 1)

    def clearHistoryWidget(self):
        self.versionLW.clear()

    def renewHistoryWidget(self):
        self.renewContentWidget(
            self.versionLW, 'detailVersionInfo',
            self.buildUpVersionItemView, reverse=1,
            outWidth=196)

    def buildUpVersionItemView(self, info, item, listWid):
        info['currentDir'] = self.dataCtrl.getDataVal('detailInnerDir')
        info['outInfoKeys'] = ['fileName', 'version']
        btnV = buttonView.ButtonView()
        btnM = buttonModel.ButtonModel('', info)
        btnC = buttonControl.ButtonControl()

        btnC.do(btnV, btnM)
        btnV.do(btnC)
        listWid.setItemWidget(item, btnV)

    def renewVersionSelection(self):
        self.versionLW.itemClicked.disconnect(self.renewVersionSelection)
        versionSelIds = []
        items = self.versionLW.selectedItems()
        popItems = items[:-2]
        selItems = items[-2:]
        for item in selItems:
            rowId = self.versionLW.row(item)
            versionSelIds.append(rowId)

        for popItem in popItems:
            popItem.setSelected(0)

        updateInfo = {'versionSelIds': versionSelIds}
        self.dataCtrl.setData(updateInfo)
        self.versionLW.itemClicked.connect(self.renewVersionSelection)
