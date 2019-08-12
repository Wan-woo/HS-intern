import sys
import difflib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
import loginPage, overallPage, setupPage, backupPage, reportFormPage, functionPage, codePage, dataPage
import backGround.testConnection

class Login(QtWidgets.QMainWindow, loginPage.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("数据比对工具")
        self.setWindowIcon(QIcon('logo.png'))
        self.isConnectionSuccess = False

    def testConnectionButton_click(self):
        host = self.dbAddressLine.text()
        username = self.usernameLine.text()
        servicename = self.servicenameLine.text()
        password = self.passwordLine.text()
        flag, msg = backGround.testConnection.connectOracle(username, password, host, servicename)
        if flag:
            reply = QMessageBox.question(self, 'Message',
                                         "连接成功!", QMessageBox.Yes, QMessageBox.Yes)
            self.isConnectionSuccess = True
            return
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "连接失败!\n失败原因为:" + msg, QMessageBox.Yes, QMessageBox.Yes)
            return

    def confirmButton_click(self):
        # 测试时可以关闭
        if not self.isConnectionSuccess:
            overallPage.show()
            login.close()
        else:
            reply = QMessageBox.question(self, 'Message',
                                         "请先通过测试连接", QMessageBox.Yes, QMessageBox.Yes)
            return



if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    # 由于进程问题，QT不允许两个相同类型的窗体进行跳转
    login = Login()
    login.show()
    # 初始化所有页面
    overallPage = overallPage.OverallPage()
    dataPage = dataPage.DataPage()
    codePage = codePage.CodePage()
    functionPage = functionPage.FunctionPage()
    reportFormPage = reportFormPage.ReportFormPage()
    backupPage = backupPage.BackupPage()
    setupPage = setupPage.SetupPage()
    # 设置pageList
    pageList = [overallPage, dataPage, codePage, functionPage, reportFormPage, backupPage, setupPage]
    for page in pageList:
        page.connectOtherPages(pageList)
    sys.exit(app.exec_())

