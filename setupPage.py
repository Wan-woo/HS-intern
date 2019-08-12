from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from resource import NavigationWidget, NavigationWidgetUp
import modelPage

class SetupPage(modelPage.Ui_MainWindow):
    def __init__(self):
        super(SetupPage, self).__init__()
        self.setupUi()
        self.tipsLabel.setText("这是设置页面")