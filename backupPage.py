from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget, NavigationWidgetUp
import modelPage

class BackupPage(modelPage.Ui_MainWindow):
    def __init__(self):
        super(BackupPage, self).__init__()
        self.setupUi()
        self.tipsLabel.setText("这是备份页面")
        # 新建一个查看备份frame和一个新建备份frame
        self.checkBackupFrame = QFrame()
        self.createBackupFrame = QFrame()
        # 新建一个查看备份Layout
        self.checkBackupLayout = QGridLayout(self.checkBackupFrame)
        # 新建一个新建备份Layout
        self.createBackupLayout = QGridLayout(self.createBackupFrame)
        # 新建一个新建备份button
        createBackupBtn = QPushButton("新建备份")
        # 为新建备份按钮添加一个槽函数
        createBackupBtn.clicked.connect(self.createBackupBtn_clicked)
        # 新建一个对比按钮
        compareBtn = QPushButton("对比")
        # 新建一个删除按钮
        deleteBtn = QPushButton("删除")
        # 新建一个显示表格
        self.backupTable = QTableWidget()
        self.backupTable.setColumnCount(4)
        self.backupTable.setHorizontalHeaderLabels([' ', '序号', '备份名', '备份日期'])
        # 新建一个横向Layout
        buttonLayout = QHBoxLayout()
        # 新建一个Layout用于右侧
        rightLayout = QVBoxLayout()
        rightLayout.setSpacing(20)

        buttonLayout.addWidget(compareBtn)
        buttonLayout.addWidget(deleteBtn)
        rightLayout.addLayout(buttonLayout)
        rightLayout.addWidget(self.backupTable)
        self.checkBackupLayout.addWidget(createBackupBtn, 1, 0)
        self.checkBackupLayout.addLayout(rightLayout, 0, 1, 3, 3)
        self.returnLayout().addWidget(self.checkBackupFrame, 1, 0, 4, 6)

    def loadData(self):
        # 此函数用于在登陆成功之后加载数据
        self.backupTable.setRowCount(12)
        self.confirmBtnGroup = QButtonGroup()
        for i in range(self.backupTable.rowCount()):
            self.confirmBtn = QRadioButton()
            self.backupTable.setCellWidget(i, 0, self.confirmBtn)
            self.confirmBtnGroup.addButton(self.confirmBtn)
            self.confirmBtnGroup.setId(self.confirmBtn, i)
        # 为按钮组添加槽函数
        self.confirmBtnGroup.buttonClicked.connect(self.confirmBtnGroup_clicked)

    def confirmBtnGroup_clicked(self):
        print(self.confirmBtnGroup.checkedId())

    def setCreateBackupFrame(self):
        # 设置左侧导航条
        self.navigationWidget = NavigationWidget.NavigationWidget()
        self.navigationWidget.setRowHeight(50)
        self.navigationWidget.setItems([u'常规', u'高级', u'管理', u'其它', u'关于'])

        # 将组件加入layout中
        self.createBackupLayout.addWidget(self.navigationWidget, 0, 0, 4, 1)

    def createBackupBtn_clicked(self):
        self.checkBackupFrame.setVisible(False)
        self.createBackupFrame.setVisible(True)

