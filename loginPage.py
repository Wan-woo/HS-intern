# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(411, 278)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 10, 301, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 80, 291, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.usernameLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.usernameLine.setObjectName("usernameLine")
        self.gridLayout.addWidget(self.usernameLine, 1, 1, 1, 1)
        self.dbAddressLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.dbAddressLine.setObjectName("dbAddressLine")
        self.gridLayout.addWidget(self.dbAddressLine, 0, 1, 1, 1)
        self.servicenameLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.servicenameLine.setObjectName("servicenameLine")
        self.gridLayout.addWidget(self.servicenameLine, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.passwordLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine.setObjectName("passwordLine")
        self.gridLayout.addWidget(self.passwordLine, 3, 1, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-40, 210, 471, 81))
        self.frame.setStyleSheet("frame{\n"
"    rgb(99, 112, 126)\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.testConnectionButton = QtWidgets.QPushButton(self.frame)
        self.testConnectionButton.setGeometry(QtCore.QRect(260, 10, 61, 21))
        self.testConnectionButton.setObjectName("testConnectionButton")
        self.confirmButton = QtWidgets.QPushButton(self.frame)
        self.confirmButton.setGeometry(QtCore.QRect(330, 10, 61, 21))
        self.confirmButton.setObjectName("confirmButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 411, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.testConnectionButton.clicked.connect(MainWindow.testConnectionButton_click)
        self.confirmButton.clicked.connect(MainWindow.confirmButton_click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "版本升级对比工具"))
        self.label_4.setText(_translate("MainWindow", "服务名"))
        self.label_2.setText(_translate("MainWindow", "数据库地址"))
        self.label_8.setText(_translate("MainWindow", "登录密码"))
        self.label_3.setText(_translate("MainWindow", "用户名"))
        self.testConnectionButton.setText(_translate("MainWindow", "测试连接"))
        self.confirmButton.setText(_translate("MainWindow", "确认"))
