from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import CheckableComboBox
import modelPage

class SetupPage(modelPage.Ui_MainWindow):
    def __init__(self):
        super(SetupPage, self).__init__()
        self.setupUi()
        # 新建设置frame、模块编辑frame和新增配置frame
        self.setupFrame = QFrame()
        self.editModuleFrame = QFrame()
        self.addSetupFrame = QFrame()
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
        self.setupTable.setColumnCount(7)
        self.setupTable.setHorizontalHeaderLabels([' ', '序号', '模块名', '名称', '类型', '影响功能', '影响指标'])

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

        # 添加槽函数
        self.editModuleBtn.clicked.connect(self.editModuleBtn_clicked)
        self.addBtn.clicked.connect(self.addBtn_clicked)

    def loadData(self):
        # 加载所有需要的数据项
        # 加载匹配项
        self.functionList = ['C', 'C++', 'Java', 'JavaScript']
        self.quotaList = ['C', 'C++', 'Java', 'JavaScript']
        self.moduleList = ['模块一', '模块二', '模块三', '模块四']
        self.processList = ['C', 'C++', 'Java', 'JavaScript']
        self.viewList = ['C', 'C++', 'Java', 'JavaScript']
        self.tableList = ['C', 'C++', 'Java', 'JavaScript']
        self.setupTable.setRowCount(12)
        self.confirmBtnGroup = QButtonGroup()
        for i in range(self.setupTable.rowCount()):
            self.confirmBtn = QRadioButton()
            self.setupTable.setCellWidget(i, 0, self.confirmBtn)
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
        self.setupFrame.setVisible(True)

    def returnBtn2_clicked(self):
        self.addSetupFrame.setVisible(False)
        self.setupFrame.setVisible(True)

    def addBtn_clicked(self):
        self.setupFrame.setVisible(False)
        self.setAddSetupFrame()
        self.addSetupFrame.setVisible(True)

    def processLineEdit_changed(self):
        self.processTable.setColumnCount(2)
        input = self.processLineEdit.text()
        i = 0
        confirmBtnGroup = QButtonGroup()
        for item in self.processList:
            if item.startswith(input):
                pass
        pass

    def setEditModuleFrame(self):
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
        self.addModuleLayout.addWidget(self.addModuleLable, alignment=Qt.AlignCenter)
        self.addModuleLayout.addLayout(self.addModuleLineLayout)
        self.addModuleLayout.addWidget(self.addModuleBtn)

        self.delModuleLable = QLabel('删除模块')
        self.delModuleLineLayout = QHBoxLayout()
        self.delModuleLineLable = QLabel('请选择删除模块名')
        self.delModuleLineText = QComboBox()
        self.delModuleLineText.setFixedWidth(150)
        self.delModuleLineLayout.addWidget(self.delModuleLineLable)
        self.delModuleLineLayout.addWidget(self.delModuleLineText)
        self.delModuleBtn = QPushButton('删除模块')
        self.delModuleLayout.addWidget(self.delModuleLable, alignment=Qt.AlignCenter)
        self.delModuleLayout.addLayout(self.delModuleLineLayout)
        self.delModuleLayout.addWidget(self.delModuleBtn)

        self.returnBtn = QPushButton('返回')
        self.returnBtn.clicked.connect(self.returnBtn_clicked)
        self.editModuleLayout.addLayout(self.juxtaposeLayout)
        self.editModuleLayout.addWidget(self.returnBtn, alignment=Qt.AlignRight)

        self.returnLayout().addWidget(self.editModuleFrame, 1, 0, 2, 5)

    def setAddSetupFrame(self):
        self.addSetupLayout = QGridLayout(self.addSetupFrame)
        self.returnBtn2 = QPushButton('返回')
        self.returnBtn2.clicked.connect(self.returnBtn2_clicked)
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
        self.processLineEdit.textChanged.connect(self.processLineEdit_changed)
        # 存储过程表格
        self.processTable = QTableWidget()
        self.viewLable = QLabel('请输入视图')
        # 视图输入框
        self.viewLineEdit = QLineEdit()
        # 视图表格
        self.viewTable = QTableWidget()
        self.tableLable = QLabel('请输入表格名')
        # 查询表格输入框
        self.tableLine = QLineEdit()
        # 查询表格的表格
        self.tableTable = QTableWidget()
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
        self.addSetupLayout.addWidget(self.tableLable, 4, 0, 1, 1, alignment=Qt.AlignRight)
        self.addSetupLayout.addWidget(self.tableLine, 4, 1, 1, 1)
        self.addSetupLayout.addWidget(self.tableTable, 5, 0, 1, 2)
        self.addSetupLayout.addWidget(self.returnBtn2, 6, 3, 1, 1)
        self.returnLayout().addWidget(self.addSetupFrame, 1, 0, 5, 5)