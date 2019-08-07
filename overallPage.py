# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overallPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(600, 400)
        MainWindow.setWindowTitle(u'导航条控件')
        mainWidget = QWidget()
        MainWindow.setCentralWidget(mainWidget)

        navigationWidget = NavigationWidget.NavigationWidget()
        navigationWidget.setRowHeight(50)
        navigationWidget.setItems([u'常规', u'高级', u'管理', u'其它', u'关于'])
        self.tipsLabel = QLabel(u"请选择：")

        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(navigationWidget, 1)
        mainLayout.addWidget(self.tipsLabel, 3, Qt.AlignCenter)

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

