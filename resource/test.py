# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         导航条控件
# Description:
# Author:       lgk
# Date:         2018/6/21
#-------------------------------------------------------------------------------

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class NavigationWidget(QWidget):
    currentItemChanged = pyqtSignal([int, str])
    def __init__(self, parent=None):
        super(NavigationWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.backgroundColor = '#E4E4E4'
        self.selectedColor = '#2CA7F8'
        self.rowHeight = 40
        self.currentIndex = 0 #当前选择的项索引
        self.listItems = []
        self.cursorIndex = -1 #当前光标所在位置的项索引

        self.setMouseTracking(True)
        self.setMinimumWidth(120)

    def addItem(self, item):
        self.listItems.append(item)
        self.update()

    def setItems(self, items):
        self.listItems = items
        self.update()

    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.update()

    def setSelectColor(self, color):
        self.selectedColor = color
        self.update()

    def setRowHeight(self, height):
        self.rowHeight = height
        self.update()

    def setCurrentIndex(self, idx):
        self.currentIndex = idx
        self.currentItemChanged.emit(idx, self.listItems[idx])
        self.update()

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        #画背景色
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.backgroundColor))
        painter.drawRect(self.rect())

        #画子项
        for i in range(len(self.listItems)):
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0, i*self.rowHeight, self.width()-1, self.rowHeight-1))

            if i == self.currentIndex:
                painter.setPen(QColor('#FFFFFF'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            elif i == self.cursorIndex:
                painter.setPen(QColor('#FFFFFF'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            else:
                painter.setPen(QColor('#202020'))
                painter.fillPath(itemPath, QColor(self.backgroundColor))

            painter.drawText(QRect(0, i*self.rowHeight, self.width(), self.rowHeight), Qt.AlignVCenter|Qt.AlignHCenter, self.listItems[i])

    def mouseMoveEvent(self, evt):
        idx = evt.y() / self.rowHeight
        if idx >= len(self.listItems):
            idx = -1
        if idx < len(self.listItems) and idx != self.cursorIndex:
            self.update()
            self.cursorIndex = int(idx)


    def mousePressEvent(self, evt):
        idx = evt.y()/self.rowHeight
        if  idx< len(self.listItems):
            self.currentIndex = int(idx)
            self.currentItemChanged.emit(int(idx), self.listItems[int(idx)])
            self.update()

    def leaveEvent(self, QEvent):
        self.cursorIndex = -1
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 400)
        self.setWindowTitle(u'导航条控件')

        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        navigationWidget = NavigationWidget()
        navigationWidget.setRowHeight(50)
        navigationWidget.setItems([u'常规', u'高级', u'管理', u'其它', u'关于'])

        self.tipsLabel = QLabel(u"请选择：")

        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(10)
        mainLayout.addWidget(navigationWidget, 1)
        mainLayout.addWidget(self.tipsLabel, 3, Qt.AlignCenter)

        navigationWidget.currentItemChanged[int, str].connect(self.slotCurrentItemChanged)
        navigationWidget.setCurrentIndex(2)

        self.show()

    def slotCurrentItemChanged(self, index, content):
        self.tipsLabel.setText(u"Current index and content：{} ---- {}".format(index, content))

def main():
    app = QApplication(sys.argv)
    mainWnd = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()