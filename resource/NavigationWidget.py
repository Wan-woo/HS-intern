from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
        self.currentIndex = -1 #当前选择的项索引
        self.listItems = []
        self.chooseItems = []
        self.checkBoxList = []
        self.cursorIndex = -1 #当前光标所在位置的项索引

        self.setMouseTracking(True)
        self.setMinimumWidth(120)

    def addItem(self, item):
        self.listItems.append(item)
        self.update()

    def setItems(self, items):
        self.listItems = items
        for i in range(len(items)):
            self.checkBoxList.append(QCheckBox(self))
            self.checkBoxList[i].move(40, self.rowHeight*i + 20)
            #self.checkBoxList[i].toggle()
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
        #self.currentItemChanged.emit(idx, self.listItems[idx])
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
            self.checkBoxList[self.currentIndex].toggle()
            self.currentItemChanged.emit(int(idx), self.listItems[int(idx)])
            self.update()

    def leaveEvent(self, QEvent):
        self.cursorIndex = -1
        self.update()

    def getChosedItems(self):
        return self.chooseItems