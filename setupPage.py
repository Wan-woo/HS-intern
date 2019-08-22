from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import CheckableComboBox
import modelPage
from backGround.setupSql import *

class SetupPage(modelPage.Ui_MainWindow):
    def __init__(self):
        super(SetupPage, self).__init__()
        self.setupUi()
        # 新建设置frame、模块编辑frame和新增配置frame
        self.setupFrame = QFrame()
        #self.addSetupFrame = QFrame()
        # 新增一个GridLayout
        self.setupLayout = QGridLayout(self.setupFrame)
        # 设置一个按钮Layout
        self.buttonLayout = QHBoxLayout()
        self.addBtn = QPushButton('新增')
        self.delBtn = QPushButton('删除')
        self.chooseLabel = QLabel('筛选')
        self.chooseComboBox = QComboBox()
        self.editModuleBtn = QPushButton('模块编辑')
        self.setupTable = QTableWidget()
        self.setupTable.setColumnCount(6)
        self.setupTable.setHorizontalHeaderLabels([' ', '模块名', '名称', '类型', '影响功能', '影响指标'])

        # 将以上组件添加进入Layout当中
        self.buttonLayout.addWidget(self.addBtn)
        self.buttonLayout.addWidget(self.delBtn)
        self.buttonLayout.addWidget(self.chooseLabel)
        self.buttonLayout.addWidget(self.chooseComboBox)
        self.buttonLayout.addWidget(self.editModuleBtn)

        # 将layout添加进入layout中
        self.setupLayout.addLayout(self.buttonLayout, 0, 0, 1, 5)
        self.setupLayout.addWidget(self.setupTable, 1, 0, 3, 5)

        # 将frame添加进入Layout中
        self.returnLayout().addWidget(self.setupFrame, 1, 0, 4, 5)
        # 设置tableName为空
        self.tableName = None
        # 添加槽函数
        self.editModuleBtn.clicked.connect(self.editModuleBtn_clicked)
        self.addBtn.clicked.connect(self.addBtn_clicked)
        self.delBtn.clicked.connect(self.delBtn_clicked)

    def loadData(self):
        # 加载所有需要的数据项
        # 加载匹配项
        self.functionList = getFunctionQuotaInfo()[0]
        self.quotaList = getFunctionQuotaInfo()[1]
        self.moduleList = getModuleInfo()
        # print(getOracleInfo())
        self.tableList = getOracleInfo()[0]
        self.processList = getOracleInfo()[1]
        self.viewList = getOracleInfo()[2]
        self.fieldTableDict = getOracleInfo()[3]
        self.setupList = getSetupList()
        # 加载
        self.chooseComboBox.clear()
        self.chooseComboBox.addItems(getModuleInfo())
        # 加载被选择列表
        self.processChooseList = []
        self.viewChooseList = []
        self.tableChooseList = []
        self.setupTable.setRowCount(len(self.setupList))
        self.confirmBtnGroup = QButtonGroup()
        for i in range(self.setupTable.rowCount()):
            self.confirmBtn = QRadioButton()
            self.setupTable.setCellWidget(i, 0, self.confirmBtn)
            self.setupTable.setItem(i, 1, QTableWidgetItem(self.setupList[i][0]))
            self.setupTable.setItem(i, 2, QTableWidgetItem(self.setupList[i][1]))
            self.setupTable.setItem(i, 3, QTableWidgetItem(self.setupList[i][2]))
            if self.setupList[i][3] == None:
                self.setupTable.setItem(i, 4, QTableWidgetItem('None'))
            else:
                self.setupTable.setItem(i, 4, QTableWidgetItem(','.join(self.setupList[i][3])))
            if self.setupList[i][4] == None:
                self.setupTable.setItem(i, 5, QTableWidgetItem('None'))
            else:
                self.setupTable.setItem(i, 5, QTableWidgetItem(','.join(self.setupList[i][4])))
            self.confirmBtnGroup.addButton(self.confirmBtn)
            self.confirmBtnGroup.setId(self.confirmBtn, i)
        # 为按钮组添加槽函数
        self.confirmBtnGroup.buttonClicked.connect(self.confirmBtnGroup_clicked)
        pass

    def confirmBtnGroup_clicked(self):
        print(self.confirmBtnGroup.checkedId())

    def editModuleBtn_clicked(self):
        self.setupFrame.setVisible(False)
        self.setEditModuleFrame()
        self.editModuleFrame.setVisible(True)

    def returnBtn_clicked(self):
        self.editModuleFrame.setVisible(False)
        self.loadData()
        self.setupFrame.setVisible(True)

    def returnBtn2_clicked(self):
        self.addSetupFrame.setVisible(False)
        self.loadData()
        self.setupFrame.setVisible(True)

    def addBtn_clicked(self):
        self.setupFrame.setVisible(False)
        self.setAddSetupFrame()
        self.addSetupFrame.setVisible(True)

    def delBtn_clicked(self):
        for i in range(self.setupTable.rowCount()):
            if self.setupTable.cellWidget(i, 0).isChecked():
                print(','.join([self.setupTable.item(i,1).text(), self.setupTable.item(i,2).text(), self.setupTable.item(i,3).text()]))
                deleteModuleList([self.setupTable.item(i,1).text(), self.setupTable.item(i,2).text(), self.setupTable.item(i,3).text()])
        self.loadData()
        pass

    def addModuleBtn_clicked(self):
        moduleName = self.addModuleLineText.text()
        if moduleName == '':
            QMessageBox.question(self, 'Message', "输入模块名不能为空", QMessageBox.Yes, QMessageBox.Yes)
            return
        elif moduleName in self.moduleList:
            QMessageBox.question(self, 'Message', "输入模块名不能重复", QMessageBox.Yes, QMessageBox.Yes)
            return
        print(moduleName)
        insertModule(moduleName)
        print('yes')
        # 先进行删除
        self.editModuleFrame.deleteLater()
        self.setEditModuleFrame()
        pass

    def delModuleBtn_clicked(self):
        moduleName = self.delModuleLineText.currentText()
        print(moduleName)
        deleteModule(moduleName)
        print('yes')
        # 先进行删除
        self.editModuleFrame.deleteLater()
        self.setEditModuleFrame()
        pass

    def processLineEdit_changed(self):
        # 如果有上次未读出的item，先读出
        for i in range(self.processTable.rowCount()):
            checkBox = self.processTable.cellWidget(i, 0)
            if checkBox.isChecked():
                item = self.processTable.item(i, 1).text()
                if item not in self.processChooseList:
                    self.processChooseList.append(item)
        # 再次初始化表格
        self.processTable.setColumnCount(2)
        self.processTable.setRowCount(0)
        input = self.processLineEdit.text()
        i = 0
        checkBoxList = []
        for item in self.processList:
            if item.startswith(str(input)):
                self.processTable.insertRow(i)
                checkBoxList.append(QCheckBox())
                self.processTable.setCellWidget(i, 0, checkBoxList[i])
                self.processTable.setItem(i, 1, QTableWidgetItem(item))
                if item in self.processChooseList:
                    checkBoxList[i].toggle()
                i += 1

    def lineEdit_changed(self, table, lineEdit, list, chooseList):
        # 如果有上次未读出的item，先读出
        for i in range(table.rowCount()):
            checkBox = table.cellWidget(i, 0)
            item = table.item(i, 1).text()
            if checkBox.isChecked():
                if item not in chooseList:
                    chooseList.append(item)
            else:
                if item in chooseList:
                    chooseList.remove(item)
        # 再次初始化表格
        table.setColumnCount(2)
        table.setRowCount(0)
        input = lineEdit.text()
        i = 0
        checkBoxList = []
        for item in list:
            if item.startswith(str(input)):
                table.insertRow(i)
                checkBoxList.append(QCheckBox())
                table.setCellWidget(i, 0, checkBoxList[i])
                table.setItem(i, 1, QTableWidgetItem(item))
                if item in chooseList:
                    checkBoxList[i].toggle()
                i += 1
        if table == self.tableTable:
            table.setColumnCount(3)
            while i >= 0:
                table.setItem(i, 2, QTableWidgetItem('点击配置'))
                i -= 1

    def tableItem_clicked(self, row, column):
        if column == 2:
            # 获取该表的字段信息
            keyField = [['1', 'id', 'int']]
            self.tableName = self.tableTable.item(row, 1).text()
            fieldList = self.fieldTableDict[self.tableName]
            self.fieldkeyTable.setColumnCount(5)
            self.fieldkeyTable.setRowCount(0)
            self.fieldkeyTable.setHorizontalHeaderLabels(['序号', '字段名', '字段类型', '是否备份', '主键选择'])
            # 添加两组checkBox
            isBackupCheckBox = []
            isKeyCheckBox = []
            i = 0
            for item in fieldList:
                self.fieldkeyTable.insertRow(i)
                self.fieldkeyTable.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                self.fieldkeyTable.setItem(i, 1, QTableWidgetItem(item))
                self.fieldkeyTable.setItem(i, 2, QTableWidgetItem('int'))
                isBackupCheckBox.append(QCheckBox())
                isKeyCheckBox.append(QCheckBox())
                self.fieldkeyTable.setCellWidget(i, 3, isBackupCheckBox[i])
                self.fieldkeyTable.setCellWidget(i, 4, isKeyCheckBox[i])
                i += 1

    def fieldKeyBtn_clicked(self):
        if self.tableName == None:
            return
        # 首先遍历这张表，收集所有的备份字段和主键
        field = []
        key = []
        for i in range(self.fieldkeyTable.rowCount()):
            if self.fieldkeyTable.cellWidget(i, 3).isChecked():
                field.append(self.fieldkeyTable.item(i, 1).text())
            if self.fieldkeyTable.cellWidget(i, 4).isChecked():
                key.append(self.fieldkeyTable.item(i, 1).text())
        if len(field) == 0 or len(key) == 0:
            reply = QMessageBox.question(self, 'Message',
                                         "备份与主键字段应多于一个", QMessageBox.Yes, QMessageBox.Yes)
            return
        flag = False
        for item in key:
            if item not in field:
                flag = True
                field.append(item)
        reply = QMessageBox.question(self, 'Message',
                                     "配置成功", QMessageBox.Yes, QMessageBox.Yes)
        # 暂时配置成功，则存储表名和表字段信息
        self.tempTableList.append(self.tableName)
        temp = {}
        temp['key'] = key
        temp['field'] = field
        self.tempReturnDict[self.tableName] = temp

    def submitSetupBtn_clicked(self):
        # 把所有数据写入
        for item in [[self.processTable, self.processChooseList], [self.viewTable, self.viewChooseList], [self.tableTable, self.tableChooseList]]:
            table = item[0]
            chooseList = item[1]
            # 如果有上次未读出的item，先读出
            for i in range(table.rowCount()):
                checkBox = table.cellWidget(i, 0)
                item = table.item(i, 1).text()
                if checkBox.isChecked():
                    if item not in chooseList:
                        chooseList.append(item)
                else:
                    if item in chooseList:
                        chooseList.remove(item)
        self.returnDict['module'] = self.moduleComboBox.currentText()
        self.returnDict['function'] = self.functionComboBox.getCheckItem()
        self.returnDict['quota'] = self.quotaComboBox.getCheckItem()
        self.returnDict['process'] = self.processChooseList
        self.returnDict['view'] = self.viewChooseList
        # 数据一致比对 查询是否所有选择的表都进行了字段配置，若没有则删除
        for tableName in self.tableChooseList:
            flag = False
            for key in self.tempReturnDict.keys():
                if tableName == key:
                    flag = True
            if not flag:
                self.tableChooseList.remove(tableName)
        self.returnDict['table'] = self.tableChooseList
        for tableName in self.tableChooseList:
            self.returnTableDict[tableName] = self.tempReturnDict[tableName]
        print(self.returnDict)
        print(self.returnTableDict)
        insertModuleObjectsField(self.returnDict, self.returnTableDict)
        # 立刻返回
        self.addSetupFrame.deleteLater()
        self.setAddSetupFrame()

    def setEditModuleFrame(self):
        self.editModuleFrame = QFrame()
        # 为frame新建一个Layout
        self.editModuleLayout = QVBoxLayout(self.editModuleFrame)
        self.editModuleLayout.setSpacing(20)
        # 新增并列Layout
        self.juxtaposeLayout = QHBoxLayout()
        # 新增模块Layout
        self.addModuleLayout = QVBoxLayout()
        self.addModuleLayout.setSpacing(40)
        self.delModuleLayout = QVBoxLayout()
        self.delModuleLayout.setSpacing(40)

        self.juxtaposeLayout.addLayout(self.addModuleLayout)
        self.juxtaposeLayout.addLayout(self.delModuleLayout)
        # 添加一个标签
        self.addModuleLable = QLabel('新增模块')
        self.addModuleLineLayout = QHBoxLayout()
        self.addModuleLineLable = QLabel('请输入新建模块名:')
        self.addModuleLineText = QLineEdit()
        self.addModuleLineText.setFixedWidth(150)
        self.addModuleLineLayout.addWidget(self.addModuleLineLable)
        self.addModuleLineLayout.addWidget(self.addModuleLineText)
        self.addModuleBtn = QPushButton('新建模块')
        self.addModuleBtn.clicked.connect(self.addModuleBtn_clicked)
        self.addModuleLayout.addWidget(self.addModuleLable, alignment=Qt.AlignCenter)
        self.addModuleLayout.addLayout(self.addModuleLineLayout)
        self.addModuleLayout.addWidget(self.addModuleBtn)

        self.delModuleLable = QLabel('删除模块')
        self.delModuleLineLayout = QHBoxLayout()
        self.delModuleLineLable = QLabel('请选择删除模块名')
        self.delModuleLineText = QComboBox()
        self.delModuleLineText.clear()
        self.delModuleLineText.addItems(getModuleInfo())
        self.delModuleLineText.setFixedWidth(150)
        self.delModuleLineLayout.addWidget(self.delModuleLineLable)
        self.delModuleLineLayout.addWidget(self.delModuleLineText)
        self.delModuleBtn = QPushButton('删除模块')
        self.delModuleBtn.clicked.connect(self.delModuleBtn_clicked)
        self.delModuleLayout.addWidget(self.delModuleLable, alignment=Qt.AlignCenter)
        self.delModuleLayout.addLayout(self.delModuleLineLayout)
        self.delModuleLayout.addWidget(self.delModuleBtn)

        self.returnBtn = QPushButton('返回')
        self.returnBtn.clicked.connect(self.returnBtn_clicked)
        self.editModuleLayout.addLayout(self.juxtaposeLayout)
        self.editModuleLayout.addWidget(self.returnBtn, alignment=Qt.AlignRight)

        self.returnLayout().addWidget(self.editModuleFrame, 1, 0, 2, 5)

    def setAddSetupFrame(self):
        # 将所有变量放置页面初始化处刷新
        # 最终数据以字典形式进行返回
        self.returnDict = {}
        # 详细的表与字段放在另一张表中
        self.returnTableDict = {}
        # 用于存放暂时配置成功的所有表名
        self.tempTableList = []
        # 用于存放暂时配置成功的表字段信息，使用双重字典
        self.tempReturnDict = {}
        self.addSetupFrame = QFrame()
        self.addSetupLayout = QGridLayout(self.addSetupFrame)
        # 增加页面返回按钮
        self.returnBtn2 = QPushButton('返回')
        self.returnBtn2.clicked.connect(self.returnBtn2_clicked)
        # 增加确认配置按钮
        self.submitSetupBtn =  QPushButton('提交配置')
        self.submitSetupBtn.clicked.connect(self.submitSetupBtn_clicked)
        self.moduleLable = QLabel('请选择模块')
        # 模块下拉选框
        self.moduleComboBox = QComboBox()
        self.moduleComboBox.addItems(self.moduleList)
        self.functionLable = QLabel('请选择功能')
        # 功能下拉多选框
        self.functionComboBox = CheckableComboBox.CheckableComboBox()
        self.functionComboBox.setItemList(self.functionList)
        self.quotaLable = QLabel('请选择指标')
        # 指标下拉多选框
        self.quotaComboBox = CheckableComboBox.CheckableComboBox()
        self.quotaComboBox.setItemList(self.quotaList)
        self.processLable = QLabel('请输入存储过程')
        # 存储过程输入框
        self.processLineEdit = QLineEdit()
        # 文本改变时触发事件
        self.processLineEdit.textChanged.connect(lambda: self.lineEdit_changed(self.processTable, self.processLineEdit, self.processList, self.processChooseList))
        # 存储过程表格
        self.processTable = QTableWidget()
        self.viewLable = QLabel('请输入视图')
        # 视图输入框
        self.viewLineEdit = QLineEdit()
        # 文本改变时触发时间
        self.viewLineEdit.textChanged.connect(lambda: self.lineEdit_changed(self.viewTable, self.viewLineEdit, self.viewList, self.viewChooseList))
        # 视图表格
        self.viewTable = QTableWidget()
        self.tableLable = QLabel('请输入表格名(先勾选，再点击配置)')
        # 查询表格输入框
        self.tableLine = QLineEdit()
        self.tableLine.textChanged.connect(lambda: self.lineEdit_changed(self.tableTable, self.tableLine, self.tableList, self.tableChooseList))
        # 查询表格的表格
        self.tableTable = QTableWidget()
        # 设置表格的选择模式为一整行
        self.tableTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 为表格添加事件响应
        self.tableTable.cellClicked.connect(self.tableItem_clicked)
        # 选择表的字段和主键
        self.fieldkeyLable = QLabel('请选择该表的字段和主键')
        self.fieldkeyTable = QTableWidget()
        # 增加一个确认配置的按钮
        self.fieldKeyBtn = QPushButton('确认该配置')
        # 为确认配置按钮添加槽函数
        self.fieldKeyBtn.clicked.connect(self.fieldKeyBtn_clicked)
        self.addSetupLayout.addWidget(self.moduleLable, 0, 0, 1, 1, alignment=Qt.AlignRight)
        self.addSetupLayout.addWidget(self.moduleComboBox, 0, 1, 1, 2)
        self.addSetupLayout.addWidget(self.functionLable, 1, 0, 1, 1, alignment=Qt.AlignRight)
        self.addSetupLayout.addWidget(self.functionComboBox, 1, 1, 1, 1)
        self.addSetupLayout.addWidget(self.quotaLable, 1, 2, 1, 1, alignment=Qt.AlignRight)
        self.addSetupLayout.addWidget(self.quotaComboBox, 1, 3, 1, 1)
        self.addSetupLayout.addWidget(self.processLable, 2, 0, 1, 1, alignment=Qt.AlignRight)
        self.addSetupLayout.addWidget(self.processLineEdit, 2, 1, 1, 1)
        self.addSetupLayout.addWidget(self.viewLable, 2, 2, 1, 1, alignment=Qt.AlignRight)
        self.addSetupLayout.addWidget(self.viewLineEdit, 2, 3, 1, 1)
        self.addSetupLayout.addWidget(self.processTable, 3, 0, 1, 2)
        self.addSetupLayout.addWidget(self.viewTable, 3, 2, 1, 2)
        self.addSetupLayout.addWidget(self.tableLable, 4, 0, 1, 1)
        self.addSetupLayout.addWidget(self.tableLine, 4, 1, 1, 1)
        self.addSetupLayout.addWidget(self.tableTable, 5, 0, 1, 2)
        self.addSetupLayout.addWidget(self.fieldkeyLable, 4, 2, 1, 1)
        self.addSetupLayout.addWidget(self.fieldKeyBtn, 4, 3, 1, 1)
        self.addSetupLayout.addWidget(self.fieldkeyTable, 5, 2, 1, 2)
        self.addSetupLayout.addWidget(self.submitSetupBtn, 6, 2, 1, 1)
        self.addSetupLayout.addWidget(self.returnBtn2, 6, 3, 1, 1)
        self.returnLayout().addWidget(self.addSetupFrame, 1, 0, 5, 5)
