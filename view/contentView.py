from alQt import QtGui
from alQt import QtCore

import basisView
import buttonView
from control import buttonControl
from model import buttonModel


class ContentView(basisView.BasisView):
    updateCmpViewSignal = QtCore.Signal(dict)
    
    def __init__(self, parent=None):
        super(ContentView, self).__init__(parent)

    def buildElements(self):
        super(ContentView, self).buildElements()
        self.contLW = QtGui.QListWidget()
        self.detailW = QtGui.QWidget()
        self.versionLW = QtGui.QListWidget()
        
        self.detailLabel = QtGui.QLabel('Detail:')
        self.historyLabel = QtGui.QLabel('History:')
        
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
        self.contLW.setMinimumWidth(180)
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
        self.clearDetailWidget()
        self.clearHistoryWidget()
        self.initEmptyDetailWidget()

    def initEmptyDetailWidget(self):
        self.detailW = QtGui.QWidget()
        self.detailW.setFixedWidth(200)
        self.detailW.setFixedHeight(200)
        self.frameLO.addWidget(self.detailW, 2, 1)

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
            info['inputJson'] = f
            item = QtGui.QListWidgetItem()

            item.setSizeHint(QtCore.QSize(
                itemSize[0], itemSize[1]))
            listWid.addItem(item)
            buildItemFunc(info, item, listWid)

    def buildUpButtonView(self, info):
        btnV = buttonView.ButtonView()
        btnM = buttonModel.ButtonModel('', info)
        btnC = buttonControl.ButtonControl()

        btnC.do(btnV, btnM)
        btnV.do(btnC)
        btnV.checkOutFileSignal.connect(self.checkOutAction)
        btnV.compareDiffVersionsSignal.connect(self.compareDiffVersionsAction)
        btnV.compareMainFileSignal.connect(self.compareDiffMainFileAction)
        return btnV

    def buildUpContItemView(self, info, item, listWid):
        info['currentDir'] = self.dataCtrl.getDataVal('currentDir')
        info['versionDetail'] = 0

        generalInfo = self.dataCtrl.getGeneralInfo()
        info.update(generalInfo)
        
        btnV = self.buildUpButtonView(info)
        listWid.setItemWidget(item, btnV)

    def showItemDetails(self, item):
        self.renewDetailVersionInfo(item)
        self.clearDetailWidget()
        self.renewDetailWidget(item)
        self.clearHistoryWidget()
        self.renewHistoryWidget()

    def renewDetailVersionInfo(self, item):
        oriBtnV = self.contLW.itemWidget(item)
        oriBtnC = oriBtnV.dataCtrl

        metaData = oriBtnC.getDataVal('metaData')
        fileName = metaData.get('fileName')
        fileType = metaData.get('fileType')
        inputJson = oriBtnC.getDataVal('inputJson')
        updateInfo = {'detailFileName': fileName,
                      'detailFileType': fileType,
                      'detailInputJson': inputJson,
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
        info['versionDetail'] = 0

        generalInfo = self.dataCtrl.getGeneralInfo()
        info.update(generalInfo)
        
        btnV = self.buildUpButtonView(info)

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
        info['versionDetail'] = 1

        generalInfo = self.dataCtrl.getGeneralInfo()
        info.update(generalInfo)
        
        btnV = self.buildUpButtonView(info)
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

    def checkOutAction(self, mess, subject, checkOutTest):
        if checkOutTest:
            # mailInfo = {'mess': mess,
            #             'subject': subject}
            # self.dataCtrl.triggerMail(mailInfo)
            self.refreshContentWidget()
            
        self.buildUpNotificationView(mess, subject)

    def buildUpNotificationView(self, mess, subject):
        QtGui.QMessageBox.warning(self, subject, mess)
        
    def refreshContentWidget(self):
        detailFileName = self.dataCtrl.getDataVal('detailFileName')
        self.dataCtrl.genDirValidContentInfo()
        self.initContent()
        self.reselectCurrentItem(detailFileName)

    def reselectCurrentItem(self, oriFileName):
        itemNum = self.contLW.count()
        for i in range(itemNum):
            item = self.contLW.item(i)
            wid = self.contLW.itemWidget(item)
            metaData = wid.dataCtrl.getDataVal('metaData')
            fileName = metaData['fileName']
            if fileName == oriFileName:
                self.showItemDetails(item)
                break
        
    def compareDiffVersionsAction(self):
        versionSelIds = self.dataCtrl.getDataVal('versionSelIds')
        if not len(versionSelIds) == 2:
            title = 'Compare Different With Two Version'
            mess = 'Must Select Two Version Files And Then Compare'
            QtGui.QMessageBox.warning(self, title, mess)
        else:
            detailVersionInfo = self.dataCtrl.getDataVal('detailVersionInfo')
            files = detailVersionInfo.keys()
            files.sort(reverse=1)
            aId = versionSelIds[0]
            bId = versionSelIds[1]
            aFile = files[aId]
            bFile = files[bId]
            diffInfo = self.dataCtrl.compareDiffFiles(aFile, bFile)
            self.emitCmpViewUpdateInfo(diffInfo)

    def compareDiffMainFileAction(self):
        versionSelIds = self.dataCtrl.getDataVal('versionSelIds')
        if not versionSelIds:
            title = 'Compare Different With Main File'
            mess = 'Must Select One Version Files And Then Compare'
            QtGui.QMessageBox.warning(self, title, mess)
        else:
            detailVersionInfo = self.dataCtrl.getDataVal('detailVersionInfo')
            files = detailVersionInfo.keys()
            files.sort(reverse=1)

            inputJson = self.dataCtrl.getDataVal('detailInputJson')
            bId = versionSelIds[1]
            aFile = inputJson
            bFile = files[bId]
            diffInfo = self.dataCtrl.compareDiffFiles(aFile, bFile)
            self.emitCmpViewUpdateInfo(diffInfo)

    def emitCmpViewUpdateInfo(self, diffInfo):
        self.updateCmpViewSignal.emit(diffInfo)
