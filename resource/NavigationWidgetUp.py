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
        self.listItems = [u'首页', u'数据对比', u'代码检查', u'功能对比', u'报表分析', u'备份', u'配置维护']
        self.checkBoxList = []
        self.cursorIndex = -1 #当前光标所在位置的项索引

        self.setMouseTracking(True)
        self.setMinimumWidth(720)
        self.itemWidth = self.width()/len(self.listItems)

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
        #painter.drawRect(self.rect())

        #画子项
        for i in range(len(self.listItems)):
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(i * self.itemWidth, 0, self.itemWidth-1, self.rowHeight-1))

            if i == self.currentIndex:
                painter.setPen(QColor('#FFFFFF'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            elif i == self.cursorIndex:
                painter.setPen(QColor('#FFFFFF'))
                painter.fillPath(itemPath, QColor(self.selectedColor))
            else:
                painter.setPen(QColor('#202020'))
                painter.fillPath(itemPath, QColor(self.backgroundColor))

            painter.drawText(QRect(int(i * self.itemWidth), 0, int(self.itemWidth), self.rowHeight), Qt.AlignVCenter|Qt.AlignHCenter, self.listItems[i])

    def mouseMoveEvent(self, evt):
        idx = evt.x() / self.itemWidth
        if idx >= len(self.listItems):
            idx = -1
        if idx < len(self.listItems) and idx != self.cursorIndex:
            self.update()
            self.cursorIndex = int(idx)


    def mousePressEvent(self, evt):
        idx = evt.x()/self.itemWidth
        if idx < len(self.listItems):
            self.currentIndex = int(idx)
            self.currentItemChanged.emit(int(idx), self.listItems[int(idx)])
            self.update()

    def leaveEvent(self, QEvent):
        self.cursorIndex = -1
        self.update()