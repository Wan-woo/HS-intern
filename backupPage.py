from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget, NavigationWidgetUp
import modelPage
import calendar
import datetime
from backGround.backupSql import *
from backGround.setupSql import *
from backGround.contrast import *

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
        # 为对比按钮增加槽函数
        compareBtn.clicked.connect(self.compareBtn_clicked)
        # 新建一个删除按钮
        deleteBtn = QPushButton("删除")
        # 为删除按钮添加槽函数
        deleteBtn.clicked.connect(self.deleteBtn_clicked)
        # 新建一个显示表格
        self.backupTable = QTableWidget()
        self.backupTable.setColumnCount(3)
        self.backupTable.setHorizontalHeaderLabels([' ', '备份名', '备份日期'])
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
        self.backupInformation = getBackupInfomation()
        self.backupTable.setRowCount(len(self.backupInformation))
        self.confirmBtnGroup = QButtonGroup()
        for i in range(self.backupTable.rowCount()):
            self.confirmBtn = QRadioButton()
            self.backupTable.setCellWidget(i, 0, self.confirmBtn)
            self.backupTable.setItem(i, 1, QTableWidgetItem(str(self.backupInformation[i][0])))
            self.backupTable.setItem(i, 2, QTableWidgetItem(str(self.backupInformation[i][1])))
            self.confirmBtnGroup.addButton(self.confirmBtn)
            self.confirmBtnGroup.setId(self.confirmBtn, i)
        # 为按钮组添加槽函数
        self.confirmBtnGroup.buttonClicked.connect(self.confirmBtnGroup_clicked)

    def confirmBtnGroup_clicked(self):
        # print(self.confirmBtnGroup.checkedId())
        pass

    def dayComboBox_changed(self, comboBox):
        comboBox.clear()
        if comboBox == self.dayComboBox1:
            self.dayComboBox1.addItems([str(x) for x in list(range(1, calendar.monthrange(
                int(self.yearComboBox1.currentText()), int(self.monthComboBox1.currentText()))[1] + 1))])
        elif comboBox == self.dayComboBox2:
            self.dayComboBox2.addItems([str(x) for x in list(range(1, calendar.monthrange(
                int(self.yearComboBox2.currentText()), int(self.monthComboBox2.currentText()))[1] + 1))])

    def setCreateBackupFrame(self):
        # 设置左侧导航条
        self.navigationWidget = NavigationWidget.NavigationWidget()
        self.navigationWidget.setRowHeight(50)
        self.navigationWidget.setItems(getModuleInfo())
        # 导航条添加槽函数
        self.navigationWidget.currentItemChanged.connect(self.navigationWidget_currentItemChanged)
        # 新建一个Layout用于安放选择日期
        self.calendarLayout = QHBoxLayout()
        # 新建combobox存放日期
        self.yearComboBox1 = QComboBox()
        self.monthComboBox1 = QComboBox()
        self.dayComboBox1 = QComboBox()
        self.yearComboBox2 = QComboBox()
        self.monthComboBox2 = QComboBox()
        self.dayComboBox2 = QComboBox()
        self.yearComboBox1.addItems([str(x) for x in list(range(2010, datetime.datetime.now().year + 1))])
        self.monthComboBox1.addItems([str(x) for x in list(range(1, 13))])
        self.yearComboBox2.addItems([str(x) for x in list(range(2010, datetime.datetime.now().year + 1))])
        self.monthComboBox2.addItems([str(x) for x in list(range(1, 13))])
        # 将年月日的初始值设置成为当日
        self.yearComboBox1.setCurrentText(str(datetime.datetime.now().year))
        self.yearComboBox2.setCurrentText(str(datetime.datetime.now().year))
        self.monthComboBox1.setCurrentText(str(datetime.datetime.now().month))
        self.monthComboBox2.setCurrentText(str(datetime.datetime.now().month))
        self.dayComboBox1.setCurrentText(str(datetime.datetime.now().day))
        self.dayComboBox2.setCurrentText(str(datetime.datetime.now().day))
        # 根据年月设置日期的范围
        self.dayComboBox1.addItems([str(x) for x in list(range(1, calendar.monthrange(
            int(self.yearComboBox1.currentText()), int(self.monthComboBox1.currentText()))[1] + 1))])
        self.dayComboBox2.addItems([str(x) for x in list(range(1, calendar.monthrange(
            int(self.yearComboBox2.currentText()), int(self.monthComboBox2.currentText()))[1] + 1))])
        # 设置槽函数，如果之前选择的选项改变，则日的范围同时改变
        self.yearComboBox1.currentTextChanged.connect(lambda: self.dayComboBox_changed(self.dayComboBox1))
        self.monthComboBox1.currentTextChanged.connect(lambda: self.dayComboBox_changed(self.dayComboBox1))
        self.yearComboBox2.currentTextChanged.connect(lambda: self.dayComboBox_changed(self.dayComboBox2))
        self.monthComboBox2.currentTextChanged.connect(lambda: self.dayComboBox_changed(self.dayComboBox2))
        # 将组件添加进入Layout
        self.calendarLayout.addWidget(QLabel('起始日期：年'))
        self.calendarLayout.addWidget(self.yearComboBox1)
        self.calendarLayout.addWidget(QLabel('月'))
        self.calendarLayout.addWidget(self.monthComboBox1)
        self.calendarLayout.addWidget(QLabel('日'))
        self.calendarLayout.addWidget(self.dayComboBox1)

        self.calendarLayout.addWidget(QLabel('终止日期：年'))
        self.calendarLayout.addWidget(self.yearComboBox2)
        self.calendarLayout.addWidget(QLabel('月'))
        self.calendarLayout.addWidget(self.monthComboBox2)
        self.calendarLayout.addWidget(QLabel('日'))
        self.calendarLayout.addWidget(self.dayComboBox2)
        # 读取数据、存储过程和视图的所有表格
        # 加载要选择备份的表
        self.tableList = getOracleInfo()[0]
        self.processList = getOracleInfo()[1]
        self.viewList = getOracleInfo()[2]
        # 创建一个Layout
        self.tableLayout = QHBoxLayout()
        self.tableVlayout = QVBoxLayout()
        self.processVLayout = QVBoxLayout()
        self.viewVLayout = QVBoxLayout()
        # 创建三个不同的table用于存放
        self.tableTable = QTableWidget()
        self.processTable = QTableWidget()
        self.viewTable = QTableWidget()
        self.tableVlayout.addWidget(QLabel('数据'), alignment=Qt.AlignCenter)
        self.tableVlayout.addWidget(self.tableTable)
        self.processVLayout.addWidget(QLabel('存储过程'), alignment=Qt.AlignCenter)
        self.processVLayout.addWidget(self.processTable)
        self.viewVLayout.addWidget(QLabel('视图'), alignment=Qt.AlignCenter)
        self.viewVLayout.addWidget(self.viewTable)
        self.tableLayout.addLayout(self.tableVlayout)
        self.tableLayout.addLayout(self.processVLayout)
        self.tableLayout.addLayout(self.viewVLayout)

        self.tableTable.setColumnCount(2)
        self.processTable.setColumnCount(2)
        self.viewTable.setColumnCount(2)
        self.tableTable.setRowCount(len(self.tableList))
        self.viewTable.setRowCount(len(self.viewList))
        self.processTable.setRowCount(len(self.processList))
        tables = [self.processTable, self.tableTable, self.viewTable]
        for table in tables:
            if table == self.processTable:
                List = self.processList
            elif table == self.tableTable:
                List = self.tableList
            elif table == self.viewTable:
                List = self.viewList
            for i in range(len(List)):
                table.setCellWidget(i, 0, QCheckBox())
                table.setItem(i, 1, QTableWidgetItem(List[i]))

        # 设置一个备份按钮
        self.submitBtn = QPushButton('备份')
        self.submitBtn.clicked.connect(self.submitBtn_clicked)

        # 设置一个返回按钮
        self.returnBtn = QPushButton('返回')
        self.returnBtn.clicked.connect(self.returnBtn_clicked)
        # 将组件加入layout中
        self.createBackupLayout.addWidget(self.navigationWidget, 0, 0, 4, 1)
        self.createBackupLayout.addLayout(self.calendarLayout, 0, 1, 1, 5)
        self.createBackupLayout.addLayout(self.tableLayout, 1, 1, 3, 5)
        self.createBackupLayout.addWidget(self.submitBtn, 4, 4, 1, 1)
        self.createBackupLayout.addWidget(self.returnBtn, 4, 5, 1, 1)
        # 将frame加入到layout当中
        self.returnLayout().addWidget(self.createBackupFrame, 1, 0, 4, 5)

    def createBackupBtn_clicked(self):
        self.checkBackupFrame.setVisible(False)
        self.setCreateBackupFrame()
        self.createBackupFrame.setVisible(True)

    def deleteBtn_clicked(self):
        for i in range(self.backupTable.rowCount()):
            if self.backupTable.cellWidget(i, 0).isChecked():
                deleteBackup(self.backupTable.item(i, 1).text())
        self.loadData()
        pass

    def returnBtn_clicked(self):
        self.createBackupFrame.setVisible(False)
        self.loadData()
        self.checkBackupFrame.setVisible(True)

    def submitBtn_clicked(self):
        tableList = []
        processList = []
        viewList = []
        for item in [[self.tableTable, tableList], [self.processTable, processList], [self.viewTable, viewList]]:
            table = item[0]
            list = item[1]
            for i in range(table.rowCount()):
                if table.cellWidget(i, 0).isChecked():
                    list.append(table.item(i, 1).text())
        startTime = self.yearComboBox1.currentText() + self.monthComboBox1.currentText().rjust(2, '0') + self.dayComboBox1.currentText().rjust(2, '0')
        endTime = self.yearComboBox2.currentText() + self.monthComboBox2.currentText().rjust(2, '0') + self.dayComboBox2.currentText().rjust(2, '0')
        createNewBackup([startTime, endTime], tableList, processList, viewList)
        # 显示备份成功的信息
        QMessageBox.question(self, 'Message', "备份成功", QMessageBox.Yes, QMessageBox.Yes)
        self.returnBtn_clicked()

    def compareBtn_clicked(self):
        # 使用QButtonGroup提供的函数更高效
        if self.confirmBtnGroup.checkedId() == -1:
            QMessageBox.question(self, 'Message', "请选择一个备份版本", QMessageBox.Yes, QMessageBox.Yes)
            return
        makeContrast(self.backupTable.item(self.confirmBtnGroup.checkedId(), 1).text())


    def navigationWidget_currentItemChanged(self):
        self.chooseModule = []
        for index, checkBox in enumerate(self.navigationWidget.checkBoxList):
            if checkBox.isChecked():
                self.chooseModule.append(self.navigationWidget.listItems[index])
        self.chooseTable = []
        self.chooseProcess = []
        self.chooseView = []
        for module in self.chooseModule:
            self.chooseTable.extend(getObjectByModule(module)[0])
            self.chooseProcess.extend(getObjectByModule(module)[1])
            self.chooseView.extend(getObjectByModule(module)[2])
        for item in [[self.chooseTable, self.tableTable], [self.chooseProcess, self.processTable], [self.chooseView, self.viewTable]]:
            chooseList = item[0]
            table = item[1]
            for i in range(table.rowCount()):
                if table.item(i, 1).text() in chooseList:
                    table.cellWidget(i, 0).setChecked(True)
                else:
                    table.cellWidget(i, 0).setChecked(False)


