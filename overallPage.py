# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overallPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget, NavigationWidgetUp
import modelPage

class Ui_MainWindow(modelPage.Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        # 设置左侧导航条
        navigationWidget = NavigationWidget.NavigationWidget()
        navigationWidget.setRowHeight(50)
        navigationWidget.setItems([u'常规', u'高级', u'管理', u'其它', u'关于'])
        # 设置多选框
        backupComboBox = QtWidgets.QComboBox()
        backupComboBox.setFixedWidth(120)
        # 设置一键生成新对比按钮
        generateButton = QtWidgets.QPushButton('一键生成新对比')
        # 设置查看已有对比的label
        backupVerLabel = QtWidgets.QLabel('备份版本1.0')
        # 设置查看之前对比的按钮
        backupVerBtn = QtWidgets.QPushButton('查看之前对比')
        # 设置表格控件
        reportTable = QtWidgets.QTableWidget()
        reportTable.setColumnCount(3)
        reportTable.setRowCount(10)
        # 将上述组件添加进入模板中
        self.returnLayout().addWidget(navigationWidget, 2, 0, 4, 1)
        self.returnLayout().addWidget(backupComboBox, 1, 1)
        self.returnLayout().addWidget(generateButton, 1, 2)
        self.returnLayout().addWidget(backupVerLabel, 1, 3)
        self.returnLayout().addWidget(backupVerBtn, 1, 4)
        self.returnLayout().addWidget(reportTable, 2, 1, 2, 3)




'''
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(600, 400)
        MainWindow.setWindowTitle(u'导航条控件')
        mainWidget = QWidget()
        MainWindow.setCentralWidget(mainWidget)
        # 设置左侧导航条
        navigationWidget = NavigationWidget.NavigationWidget()
        navigationWidget.setRowHeight(50)
        navigationWidget.setItems([u'常规', u'高级', u'管理', u'其它', u'关于'])
        # 设置上方导航条
        navigationWidgetUp = NavigationWidgetUp.NavigationWidget()
        navigationWidgetUp.setRowHeight(50)

        self.tipsLabel = QLabel(u"请选择：")

        mainLayout = QGridLayout(mainWidget)

        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(navigationWidget, 2, 0, 4, 1)
        mainLayout.addWidget(navigationWidgetUp, 0, 0, 1, 6)
        mainLayout.addWidget(self.tipsLabel, 1, 1, 4, 5, Qt.AlignCenter)

        navigationWidget.currentItemChanged[int, str].connect(self.slotCurrentItemChanged)
        navigationWidget.setCurrentIndex(-1)

        #self.gridLayout.addWidget(self, navigationWidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def slotCurrentItemChanged(self, index, content):
        self.tipsLabel.setText(u"Current index and content：{} ---- {}".format(index, content))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
'''
