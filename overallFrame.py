from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget, NavigationWidgetUp


def setup(self):
    # 在init方法中，预先生成要用到的组件
    self.reportFrame = QFrame()

    # 采用设置frame的方法构造页面
    self.normalFrame = QFrame()
    self.normalFrame.setStyleSheet("QFrame{border: 0px;};")
    self.normalFrameLayout = QGridLayout(self.normalFrame)
    # 设置左侧导航条
    self.navigationWidget = NavigationWidget.NavigationWidget()
    self.navigationWidget.setRowHeight(50)
    self.navigationWidget.setItems([u'常规', u'高级', u'管理', u'其它', u'关于'])
    # 设置多选框
    self.backupComboBox = QtWidgets.QComboBox()
    self.backupComboBox.setFixedWidth(120)
    # 设置一键生成新对比按钮
    self.generateButton = QPushButton('一键生成新对比')
    # 设置查看已有对比的label
    self.backupVerLabel = QtWidgets.QLabel('备份版本1.0')
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
    self.generateButton.clicked.connect(showTable)


# 设置函数，按下一键对比按钮，显示表格内容
def showTable(self):
    # 设置表格控件
    reportTable = QtWidgets.QTableWidget()
    reportTable.setColumnCount(3)
    reportTable.setRowCount(12)
    reportTable.setColumnWidth(0, 150)
    reportTable.setColumnWidth(1, 150)
    reportTable.setColumnWidth(2, 150)
    # 设置表格控件最后一列为按钮
    # 创建一个按钮组，将所有按钮加入进去
    confirmBtnGroup = QButtonGroup()
    for i in range(reportTable.rowCount()):
        confirmBtn = QPushButton('查看')
        confirmBtn.setCheckable(True)
        confirmBtn.setStyleSheet("QPushButton{margin-left:20px;margin-right:20px;};")
        reportTable.setCellWidget(i, 2, self.confirmBtn)
        confirmBtnGroup.addButton(self.confirmBtn)
        confirmBtnGroup.setId(self.confirmBtn, i)
    # 为按钮组添加槽函数
    confirmBtnGroup.buttonClicked.connect(confirmBtnGroup_clicked)
    # 将上述组件添加进入frame中
    self.normalFrameLayout.addWidget(reportTable, 1, 1, 3, 4)


def confirmBtnGroup_clicked(self):
    if self.confirmBtnGroup.checkedId() != -1:
        self.normalFrame.setVisible(False)
        self.setReportFrame(self.confirmBtnGroup.checkedId())
        self.reportFrame.setVisible(True)


def setReportFrame(self, checkedId):
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
    dataTable.setColumnCount(3)
    dataTable.setRowCount(10)
    # 创建一个查看按钮
    dataConfirmBtn = QPushButton('查看')
    dataConfirmBtn.setFixedHeight(15)
    dataConfirmBtn.setStyleSheet("QPushButton{margin-left:50px;margin-right:50px;};")
    # 将所有组件添加到其中
    dataLayout.addWidget(dataLabel, alignment=Qt.AlignCenter)
    dataLayout.addWidget(dataTable)
    dataLayout.addWidget(dataConfirmBtn)
    # 创建视图/存储过程Layout
    viewprocessLayout = QVBoxLayout()
    viewprocessLayout.setSpacing(10)
    viewprocessLabel = QLabel('视图/存储过程对比')
    viewprocessTable = QTableWidget()
    viewprocessTable.setColumnCount(3)
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
    funcreportTable.setColumnCount(3)
    funcreportBtn = QPushButton('查看')
    funcreportBtn.setFixedHeight(15)
    funcreportBtn.setStyleSheet("QPushButton{margin-left:50px;margin-right:50px;};")
    funcreportLayout.addWidget(funcreportLable, alignment=Qt.AlignCenter)
    funcreportLayout.addWidget(funcreportTable)
    funcreportLayout.addWidget(funcreportBtn)

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