from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget, NavigationWidgetUp
import modelPage

class CodePage(modelPage.Ui_MainWindow):
    def __init__(self):
        super(CodePage, self).__init__()
        self.setupUi()
        self.tipsLabel.setText("这是代码页面")