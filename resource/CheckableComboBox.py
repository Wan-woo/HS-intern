from PyQt5 import QtCore, QtGui, QtWidgets
#
class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))
        self.itemList = []
        self.setEditable(True)
        self.activated.connect(self.lineShow)

    def lineShow(self):
        self.lineEdit().setText(';'.join(self.getCheckItem()))

    def setItemList(self, itemList):
        self.itemList = itemList
        for index, element in enumerate(itemList):
            self.addItem(element)
            item = self.model().item(index, 0)
            item.setCheckState(QtCore.Qt.Unchecked)

    def clearItemPressed(self):
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Unchecked)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
    def getCheckItem(self):
        #getCheckItem可以获得选择的项目text
        checkedItems = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                checkedItems.append(item.text())
        return checkedItems
    def checkedItems(self):
        checkedItems = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == QtCore.Qt.Checked:
                checkedItems.append(item)
        return checkedItems
