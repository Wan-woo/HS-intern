import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ProgressBar(QDialog):
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)
        self.resize(350, 100)
        self.setWindowTitle(self.tr("Processing progress"))
        self.centerLayout = QHBoxLayout()
        self.progressBar = QProgressBar()
        self.lable = QLabel()
        self.centerLayout.addWidget(self.progressBar)
        self.centerLayout.addWidget(self.lable)
        self.setLayout(self.centerLayout)

    def changeValue(self, i):
        self.progressBar.setValue(i)
        self.lable.setText(str(i))

    def closeDialog(self):
        self.close()


class Worker(QThread):

    progressBarValue = pyqtSignal(int)  # 更新进度条

    def __init__(self):
        super(Worker, self).__init__()


    def run(self):
        for i in range(101):
            time.sleep(0.1)
            self.progressBarValue.emit(i)  # 发送进度条的值 信号

