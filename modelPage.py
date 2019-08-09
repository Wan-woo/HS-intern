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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(600, 400)
        MainWindow.setWindowTitle(u'导航条控件')
        mainWidget = QWidget()
        MainWindow.setCentralWidget(mainWidget)

        # 设置上方导航条
        navigationWidgetUp = NavigationWidgetUp.NavigationWidget()
        navigationWidgetUp.setRowHeight(50)

        self.tipsLabel = QLabel(u"请选择：")

        self.mainLayout = QGridLayout(mainWidget)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        #self.mainLayout.setSpacing(10)
        self.mainLayout.addWidget(navigationWidgetUp, 0, 0, 1, 6)
        self.mainLayout.addWidget(self.tipsLabel, 1, 1, 4, 5, Qt.AlignCenter)

        #self.gridLayout.addWidget(self, navigationWidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def slotCurrentItemChanged(self, index, content):
        self.tipsLabel.setText(u"Current index and content：{} ---- {}".format(index, content))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def returnLayout(self):
        return self.mainLayout
