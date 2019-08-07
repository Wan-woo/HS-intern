# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overallPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from resource.NavigationWidget import NavigationWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(647, 403)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBox = QtWidgets.QToolBox()
        self.toolBox.addItem(QtWidgets.QPushButton("Tab Content 1"), "Tab &1")
        self.toolBox.addItem(QtWidgets.QLabel("Tab Content 2"), "Tab &2")
        self.toolBox.setCurrentIndex(0)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        navigationWidget = NavigationWidget()
        navigationWidget.listItems = ["a", "b", "c"]
        navigationWidget.rowHeight = 50


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
