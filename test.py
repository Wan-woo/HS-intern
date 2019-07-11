import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon
#from qtpy import QtWidgets
#from qtpy.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
#from qtpy.QtGui import QIcon
from myFirstWindow import Ui_MainWindow
import qtpy.QtWidgets

class MyForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("数据比对工具")
        self.setWindowIcon(QIcon('logo.png'))

    def pushButton_click(self):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(2)
        i = 0
        j = 0
        columnWidth = self.tableWidget.width() / self.tableWidget.columnCount()
        rowHeight = self.tableWidget.height() / self.tableWidget.rowCount()
        value = 'test'
        self.tableWidget.setItem(i, j, QTableWidgetItem(value))
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        #self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setVisible(True)

    def exitButton_click(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            quit()
        else:
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myForm = MyForm()
    myForm.show()
    sys.exit(app.exec_())
