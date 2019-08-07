from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class NavigationWidget(QWidget):
    def __init__(self, parent=None):
        super(NavigationWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.backgroundColor = QColor(41, 47, 56)
        self.selectedColor = QColor(29, 32, 37)
        self.indictorBarColor = QColor(2, 160, 235)
        self.textColor1 = QColor(226, 240, 252)
        self.textColor2 = QColor(104, 118, 130)
        self.rowHeight = 40
        self.currentIndex = 0
        self.listItems = []
        self.cursorIndex = -1

        self.setMouseTracking(True)
        self.setMinimumWidth(120)

    def mousePressEvent(self, evt):
        idx = evt.y()/self.rowHeight
        if idx < len(self.listItems):
            self.currentIndex = idx
            self.currentItemChanged.emit(idx, self.listItems[idx])
            self.update()

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.backgroundColor))
        painter.drawRect(self.rect())

        for i in range(len(self.listItems)):
            itemPath = QPainterPath()
            itemPath.addRect(QRectF(0,i*self.rowHeight,self.width()-1), self.rowHeight-1)
            indictorBarPath = QPainterPath()
            indictorBarPath.addRect(QRectF(0, i*self.rowHeight, 5, self.rowHeight-1))

            if i==self.currentIndex or i==self.cursorIndex:
                painter.setPen(self.textColor1)
                painter.fillPath(itemPath, QColor(self.selectedColor))
                painter.fillPath(indictorBarPath, QColor(self.indictorBarColor))
            else:
                painter.setPen(self.textColor2)
                painter.fillPath(itemPath, QColor(self.backgroundColor))

            painter.drawText(QRect(0,i*self.rowHeight, self.width(),self.rowHeight),Qt.AlignVCenter|Qt.AlignHCenter, self.listItems[i])