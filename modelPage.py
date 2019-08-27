# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overallPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidgetUp
from backGround.setupSql import *
from backGround.backupSql import *
from backGround.overViewSql import *
from backGround.contrast import *

class Ui_MainWindow(QtWidgets.QMainWindow):
    moduleInfo = []
    backupInformation = []
    moduleResult = []
    contrastInfo = []
    functionQuotaInfo = []
    oracleInfo = []
    setupList = []

    # 继承初始化，需要将相关的变量在这里初始化
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        # 使用一个list存储所有的pages，方便之后的切换与连接
        self.pageList = []
    def setupUi(self):
        self.resize(600, 480)
        self.setWindowTitle(u'导航条控件')
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        # 设置上方导航条
        navigationWidgetUp = NavigationWidgetUp.NavigationWidget()
        navigationWidgetUp.setRowHeight(50)
        navigationWidgetUp.currentItemChanged.connect(self.slotCurrentItemChanged)

        self.tipsLabel = QLabel(u"请选择：")

        self.mainLayout = QGridLayout(mainWidget)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        #self.mainLayout.setSpacing(10)
        self.mainLayout.addWidget(navigationWidgetUp, 0, 0, 1, 6)
        self.mainLayout.addWidget(self.tipsLabel, 1, 1, 4, 5, Qt.AlignCenter)

        #self.gridLayout.addWidget(self, navigationWidget)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def slotCurrentItemChanged(self, index, content):
        self.close()
        self.pageList[index].loadData()
        self.update()
        self.pageList[index].show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def returnLayout(self):
        return self.mainLayout

    def connectOtherPages(self, pageList):
        # 连接所有页面 pageList = [overallPage, dataPage, codePage, functionPage, reportFormPage, backupPage, setupPage]
        self.pageList = pageList

    def loadData(self):
        # 此函数一般用于加载首个页面的动态数据
        pass

    def data_transform(self):
        pass

    @classmethod
    def cls_loadData(cls):
        Ui_MainWindow.moduleInfo = getModuleInfo()
        Ui_MainWindow.backupInformation = getBackupInfomation()
        Ui_MainWindow.moduleResult = getModuleResult()
        Ui_MainWindow.contrastInfo = getCurContrastInfo()
        Ui_MainWindow.functionQuotaInfo = getFunctionQuotaInfo()
        Ui_MainWindow.oracleInfo = getOracleInfo()
        Ui_MainWindow.setupList = getSetupList()
