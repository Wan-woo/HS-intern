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