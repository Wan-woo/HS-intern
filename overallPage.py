# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overallPage.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget
from resource import ProgressBar
import modelPage
from backGround.setupSql import *
from backGround.backupSql import *
from backGround.overViewSql import *
from backGround.contrast import *
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"  # 日期格式
fp = logging.FileHandler('log.txt', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])  # 调用

class OverallPage(modelPage.Ui_MainWindow):
    def __init__(self):
        super(OverallPage, self).__init__()
        self.setupUi()
        # 在init方法中，预先生成要用到的组件
        self.reportFrame = QFrame()

        # 采用设置frame的方法构造页面
        self.normalFrame = QFrame()
        self.normalFrame.setStyleSheet("QFrame{border: 0px;};")
        self.normalFrameLayout = QGridLayout(self.normalFrame)
        # 设置左侧导航条
        self.navigationWidget = NavigationWidget.NavigationWidget()
        # 设置多选框
        self.backupComboBox = QtWidgets.QComboBox()
        self.backupComboBox.setFixedWidth(120)
        # 设置一键生成新对比按钮
        self.generateButton = QPushButton('一键生成新对比')
        # 设置查看已有对比的label
        self.backupVerLabel = QtWidgets.QLabel()
        # 设置查看之前对比的按钮
        self.backupVerBtn = QtWidgets.QPushButton('查看之前对比')
        # 将上述组件加入模板
        self.normalFrameLayout.addWidget(self.navigationWidget, 0, 0, 4, 1)
        self.normalFrameLayout.addWidget(self.backupComboBox, 0, 1)
        self.normalFrameLayout.addWidget(self.generateButton, 0, 2)
        self.normalFrameLayout.addWidget(self.backupVerLabel, 0, 3)
        self.normalFrameLayout.addWidget(self.backupVerBtn, 0, 4)
        self.returnLayout().addWidget(self.normalFrame, 1, 0, 4, 5)
        # 设置槽函数，显示表格
        self.generateButton.clicked.connect(lambda: self.showTable(True))
        self.backupVerBtn.clicked.connect(lambda: self.showTable(False))

    def loadData(self):
        self.navigationWidget.setItems(self.moduleInfo)
        self.backupComboBox.clear()
        for item in self.backupInformation:
            self.backupComboBox.addItem(str(item[0]))
        if len(self.moduleResult) == 0:
            self.backupVerLabel.setText('无备份版本')
            QMessageBox.question(self, 'Message',
                                 '请先前往备份页面进行备份', QMessageBox.Yes, QMessageBox.Yes)
            self.close()
            self.pageList[5].loadData()
            self.update()
            self.pageList[5].show()
        else:
            self.backupVerLabel.setText('备份版本'+str(self.moduleResult[0]))
        pass

    # 设置函数，按下一键对比按钮，显示表格内容
    def showTable(self, newCompare):
        # 在此处进行测试
        self.progressBar = ProgressBar.ProgressBar()
        worker = ProgressBar.Worker()
        worker.progressBarValue.connect(self.progressBar.changeValue)
        worker.start()
        self.progressBar.exec_()
        # 首先判断展示是使用已有的对比还是重新对比
        alreadyComparedVersion = self.moduleResult[0]
        if newCompare:
            if alreadyComparedVersion != self.backupComboBox.currentText():
                makeContrast(self.backupComboBox.currentText())
                modelPage.Ui_MainWindow.moduleResult = getModuleResult()
                modelPage.Ui_MainWindow.contrastInfo = getCurContrastInfo()
                self.loadData()
        # 设置表格控件
        self.reporTable = QtWidgets.QTableWidget()
        self.reporTable.setColumnCount(3)
        self.reporTable.setHorizontalHeaderLabels(['模块名', '差异结果', '查看按钮'])
        self.reporTable.setColumnWidth(0, 150)
        self.reporTable.setColumnWidth(1, 150)
        self.reporTable.setColumnWidth(2, 150)
        # 设置表格的行数
        self.reporTable.setRowCount(len(self.moduleResult[1]))
        # 设置表格控件最后一列为按钮
        # 创建一个按钮组，将所有按钮加入进去
        self.confirmBtnGroup = QButtonGroup()
        i = 0
        for key in self.moduleResult[1].keys():
            self.confirmBtn = QPushButton('查看')
            self.confirmBtn.setCheckable(True)
            self.confirmBtn.setStyleSheet("QPushButton{margin-left:20px;margin-right:20px;};")
            self.reporTable.setCellWidget(i, 2, self.confirmBtn)
            self.confirmBtnGroup.addButton(self.confirmBtn)
            self.confirmBtnGroup.setId(self.confirmBtn, i)
            # 设置第一列模块名
            self.reporTable.setItem(i, 0, QTableWidgetItem(key))
            output = '共有'+str(len(self.moduleResult[1][key]))+'张表存在不同,'
            output += '共有' + str(len(self.moduleResult[2][key])) + '个存储过程存在不同,'
            output += '共有' + str(len(self.moduleResult[3][key])) + '张视图存在不同.'
            self.reporTable.setItem(i, 1, QTableWidgetItem(output))
            i += 1
        # 为按钮组添加槽函数
        self.confirmBtnGroup.buttonClicked.connect(self.confirmBtnGroup_clicked)
        # 将上述组件添加进入frame中
        self.normalFrameLayout.addWidget(self.reporTable, 1, 1, 3, 4)


    def confirmBtnGroup_clicked(self):
        if self.confirmBtnGroup.checkedId() != -1:
            self.normalFrame.setVisible(False)
            self.setReportFrame(self.reporTable.item(self.confirmBtnGroup.checkedId(), 0).text())
            self.reportFrame.setVisible(True)

    def setReportFrame(self, moduleName):
        reportFrameLayout = QVBoxLayout(self.reportFrame)
        threeReportFrameLayout = QHBoxLayout()
        threeReportFrameLayout.setSpacing(30)
        # 创建数据板块Layout
        dataLayout = QVBoxLayout()
        dataLayout.setSpacing(10)
        # 创建一个label
        dataLabel = QLabel('数据对比')
        # 创建一个数据表格
        dataTable = QTableWidget()
        dataTable.setColumnCount(1)
        dataTable.setRowCount(10)
        # 创建一个查看按钮
        dataConfirmBtn = QPushButton('查看')
        dataConfirmBtn.setFixedHeight(15)
        dataConfirmBtn.setStyleSheet("QPushButton{margin-left:50px;margin-right:50px;};")
        dataConfirmBtn.clicked.connect(lambda: self.dataConfirmBtn_clicked(self.moduleResult[1][moduleName]))
        # 将所有组件添加到其中
        dataLayout.addWidget(dataLabel, alignment=Qt.AlignCenter)
        dataLayout.addWidget(dataTable)
        dataLayout.addWidget(dataConfirmBtn)
        # 创建视图/存储过程Layout
        viewprocessLayout = QVBoxLayout()
        viewprocessLayout.setSpacing(10)
        viewprocessLabel = QLabel('视图/存储过程对比')
        viewprocessTable = QTableWidget()
        viewprocessTable.setColumnCount(1)
        viewprocessBtn = QPushButton('查看')
        viewprocessBtn.setStyleSheet("QPushButton{margin-left:50px;margin-right:50px;};")
        viewprocessBtn.setFixedHeight(15)
        viewprocessLayout.addWidget(viewprocessLabel, alignment=Qt.AlignCenter)
        viewprocessLayout.addWidget(viewprocessTable)
        viewprocessLayout.addWidget(viewprocessBtn)
        # 创建功能/报表layout
        funcreportLayout = QVBoxLayout()
        funcreportLayout.setSpacing(10)
        funcreportLable = QLabel('功能/报表对比')
        funcreportTable = QTableWidget()
        funcreportTable.setColumnCount(1)
        funcreportBtn = QPushButton('查看')
        funcreportBtn.setFixedHeight(15)
        funcreportBtn.setStyleSheet("QPushButton{margin-left:50px;margin-right:50px;};")
        funcreportLayout.addWidget(funcreportLable, alignment=Qt.AlignCenter)
        funcreportLayout.addWidget(funcreportTable)
        funcreportLayout.addWidget(funcreportBtn)

        # 向三张表格增加数据
        dataTable.setRowCount(len(self.moduleResult[1][moduleName]))
        viewprocessTable.setRowCount(len(self.moduleResult[2][moduleName]))
        funcreportTable.setRowCount(len(self.moduleResult[3][moduleName]))
        for item in [[dataTable, self.moduleResult[1][moduleName]], [viewprocessTable, self.moduleResult[2][moduleName]], [funcreportTable, self.moduleResult[3][moduleName]]]:
            table = item[0]
            i = 0
            for name in item[1]:
                table.setItem(i, 0, QTableWidgetItem(name))
                i += 1
        # 设置一个返回按钮
        returnBtn = QPushButton('返回')
        returnBtn.setMinimumWidth(100)
        returnBtn.clicked.connect(self.returnBtn_clicked)
        # 上述组件添加进入layout中
        threeReportFrameLayout.addLayout(dataLayout)
        threeReportFrameLayout.addLayout(viewprocessLayout)
        threeReportFrameLayout.addLayout(funcreportLayout)
        reportFrameLayout.addLayout(threeReportFrameLayout)
        reportFrameLayout.addWidget(returnBtn, alignment=Qt.AlignRight)
        self.returnLayout().addWidget(self.reportFrame, 1, 0, 4, 6)


    def returnBtn_clicked(self):
        self.reportFrame.setVisible(False)
        self.normalFrame.setVisible(True)

    def dataConfirmBtn_clicked(self, tableList):
        self.close()
        self.pageList[1].show()
        logging.info(tableList)
        self.pageList[1].loadTableInfo(tableList)