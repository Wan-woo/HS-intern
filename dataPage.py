from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget, NavigationWidgetUp
import modelPage
from backGround.contrast import *

class DataPage(modelPage.Ui_MainWindow):
    def __init__(self):
        super(DataPage, self).__init__()
        self.setupUi()
        self.tipsLabel.setText("这是数据页面")

        # 设置一个横向的Layout
        self.inputLayout = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.isClearButtonEnabled()
        self.queryBtn = QPushButton('确认查找')
        self.queryBtn.clicked.connect(self.queryBtn_clicked)
        self.inputLayout.addWidget(QLabel('请输入表名'))
        self.inputLayout.addWidget(self.lineEdit)
        self.inputLayout.addWidget(self.queryBtn)
        self.inputLayout.addStretch(0.5)
        self.compareTable = QTableWidget()
        self.compareTable.setColumnCount(8)
        self.compareTable.setHorizontalHeaderLabels(['选择', '备份表', '升级表', 'Delete', 'Insert', 'Same', 'Update', 'Message'])
        self.compareTable.setMaximumHeight(100)

        self.comboBox = QComboBox()
        self.comboBox.addItems(['Delete', 'Insert', 'Same', 'Update', 'Difference', 'All'])
        self.comboBox.setCurrentIndex(4)
        self.comboBox.setFixedWidth(120)

        # 选择表格总共有多少页，初始化为0
        self.pageNum = 0
        # 在没有选择要对比的表格之前， 所有的按钮都不可使用，避免出错
        self.firstpageBtn = QPushButton('首页')
        self.firstpageBtn.clicked.connect(self.firstpageBtn_clicked)
        self.firstpageBtn.setEnabled(False)
        self.lastpageBtn = QPushButton('上一页')
        self.lastpageBtn.clicked.connect(self.lastpageBtn_clicked)
        self.lastpageBtn.setEnabled(False)
        self.pageLable = QLabel('1')
        self.nextpageBtn = QPushButton('下一页')
        self.nextpageBtn.clicked.connect(self.nextpageBtn_clicked)
        self.nextpageBtn.setEnabled(False)
        self.finalpageBtn = QPushButton('尾页')
        self.finalpageBtn.clicked.connect(self.finalpageBtn_clicked)
        self.finalpageBtn.setEnabled(False)
        self.pageTotal = QLabel('共10页')
        self.pageLineEdit = QLineEdit()
        self.pageLineEdit.setEnabled(False)
        self.jumpBtn = QPushButton('跳转')
        self.jumpBtn.clicked.connect(self.jumpBtn_clicked)
        self.jumpBtn.setEnabled(False)
        self.downLayout = QHBoxLayout()
        self.downLayout.addWidget(self.comboBox)
        self.downLayout.addWidget(self.firstpageBtn)
        self.downLayout.addWidget(self.lastpageBtn)
        self.downLayout.addWidget(self.pageLable)
        self.downLayout.addWidget(self.nextpageBtn)
        self.downLayout.addWidget(self.finalpageBtn)
        self.downLayout.addWidget(self.pageTotal)
        self.downLayout.addWidget(self.pageLineEdit)
        self.downLayout.addWidget(self.jumpBtn)

        self.oldTableLayout = QVBoxLayout()
        self.newTableLayout = QVBoxLayout()
        self.oldTable = QTableWidget()
        self.newTable = QTableWidget()
        self.oldTableLayout.addWidget(QLabel('备份表'), alignment=Qt.AlignCenter)
        self.oldTableLayout.addWidget(self.oldTable)
        self.newTableLayout.addWidget(QLabel('新表'), alignment=Qt.AlignCenter)
        self.newTableLayout.addWidget(self.newTable)

        self.upLayout = QVBoxLayout()
        self.upLayout.addLayout(self.inputLayout)
        self.upLayout.addWidget(self.compareTable)
        self.upLayout.addLayout(self.downLayout)
        self.returnLayout().addLayout(self.upLayout, 1, 1, 1, 4)
        self.returnLayout().addLayout(self.oldTableLayout, 2, 0, 3, 3)
        self.returnLayout().addLayout(self.newTableLayout, 2, 3, 3, 3)

    def loadData(self):
        self.contrastInfo = getCurContrasrInfo()
        # 设置一个带匹配功能的输入框
        self.matchString = self.contrastInfo[1]
        self.lineEdit.setCompleter(QCompleter(self.matchString))
        pass

    def loadTableInfo(self):
        pass

    # 该函数用于刷新详细内容的表格
    def loadTableData(self, page):
        # 获取差异类型
        type = self.comboBox.currentText()

    def queryBtn_clicked(self):
        tableName = self.lineEdit.text()
        if tableName not in self.matchString:
            QMessageBox.question(self, 'Message', "未查找到所需的表", QMessageBox.Yes, QMessageBox.Yes)
            return
        tableContrastResult = self.contrastInfo[5][tableName]
        self.compareTable.setRowCount(1)
        radioBtn = QRadioButton()
        radioBtn.clicked.connect(lambda: self.buttonGroup_clicked(tableName))
        self.compareTable.setCellWidget(0, 0, radioBtn)
        self.compareTable.setItem(0, 1, QTableWidgetItem(tableName))
        self.compareTable.setItem(0, 2, QTableWidgetItem(tableName))
        self.compareTable.setItem(0, 3, QTableWidgetItem(str(tableContrastResult[0])))
        self.compareTable.setItem(0, 4, QTableWidgetItem(str(tableContrastResult[1])))
        self.compareTable.setItem(0, 5, QTableWidgetItem(str(tableContrastResult[2])))
        self.compareTable.setItem(0, 6, QTableWidgetItem(str(tableContrastResult[3])))

    def buttonGroup_clicked(self, tableName):
        self.firstpageBtn.setEnabled(True)
        self.lastpageBtn.setEnabled(True)
        self.nextpageBtn.setEnabled(True)
        self.finalpageBtn.setEnabled(True)
        self.pageLineEdit.setEnabled(True)
        self.jumpBtn.setEnabled(True)
        self.oldTable.setColumnCount(len(self.contrastInfo[4][tableName]))
        self.oldTable.setHorizontalHeaderLabels(self.contrastInfo[4][tableName])
        self.newTable.setColumnCount(len(self.contrastInfo[4][tableName]))
        self.newTable.setHorizontalHeaderLabels(self.contrastInfo[4][tableName])
        # 开始对数据进行展示,首先确定页面数量
        if self.comboBox.currentIndex() < 4:
            self.pageNum = self.contrastInfo[5][tableName][self.comboBox.currentIndex()] / 30
        elif self.comboBox.currentIndex() == 4:
            self.pageNum = (self.contrastInfo[5][tableName][0] + self.contrastInfo[5][tableName][1] + self.contrastInfo[5][tableName][3]) / 30
        else:
            self.pageNum = sum(self.contrastInfo[5][tableName]) / 30
        self.pageNum = int(self.pageNum) + 1
        self.pageTotal.setText('共' + str(self.pageNum) + '页')
        self.pageTotal.setText(str(self.pageNum))
        getContrastData(tableName, self.comboBox.currentIndex(), int(self.pageLable.text()))
        oldTableList, newTableList = getContrastData(tableName, self.comboBox.currentIndex(), int(self.pageLable.text()))
        self.oldTable.setRowCount(len(oldTableList))
        self.newTable.setRowCount(len(newTableList))
        for i in range(len(oldTableList)):
            oldItem = oldTableList[i]
            newItem = newTableList[i]
            for j in range(len(oldItem)):
                self.oldTable.setItem(i, j, QTableWidgetItem(oldItem[j]))
                self.newTable.setItem(i, j, QTableWidgetItem(newItem[j]))
        pass

    def firstpageBtn_clicked(self):
        self.pageLable.setText('1')
        self.loadTableData(1)

    def lastpageBtn_clicked(self):
        if int(self.pageLable.text()) == 1:
            QMessageBox.question(self, 'Message', "已经是第一页", QMessageBox.Yes, QMessageBox.Yes)
            return
        page = int(self.pageLable.text()) - 1
        self.pageLable.setText(str(page))
        self.loadTableData(page)

    def nextpageBtn_clicked(self):
        if int(self.pageLable.text()) == self.pageNum:
            QMessageBox.question(self, 'Message', "已经是最后一页", QMessageBox.Yes, QMessageBox.Yes)
            return
        page = int(self.pageLable.text()) + 1
        self.pageLable.setText(str(page))
        self.loadTableData(page)

    def finalpageBtn_clicked(self):
        self.pageLable.setText(str(self.pageNum))
        self.loadTableData(self.pageNum)

    def jumpBtn_clicked(self):
        if not self.pageLineEdit.text().isdecimal():
            QMessageBox.question(self, 'Message', "不是合法输入", QMessageBox.Yes, QMessageBox.Yes)
            self.pageLineEdit.clear()
            return
        page = int(self.pageLineEdit.text())
        if page < 1 or page > self.pageNum:
            QMessageBox.question(self, 'Message', "超出页面范围", QMessageBox.Yes, QMessageBox.Yes)
            self.pageLineEdit.clear()
            return
        self.pageLable.setText(str(page))
        self.loadTableData(page)
