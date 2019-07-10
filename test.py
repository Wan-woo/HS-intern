import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from myFirstWindow import Ui_Form



class MyForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("数据比对工具")
        self.setWindowIcon(QIcon('logo.png'))

    def pushButton_click(self):
        self.textEdit.setText("你点击了按钮")

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
