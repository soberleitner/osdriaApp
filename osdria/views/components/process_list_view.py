from PySide2.QtWidgets import *
from PySide2.QtCore import Signal, QObject, QAbstractListModel, Qt, QModelIndex
from models.data_structure import Dict


class ProcessListView(QListView):
    """define functionality of list views in process dialog"""
    edit_add = Signal([str, int, QObject])
    #edit_process = Signal(int)

    def __init__(self, parent):
        super(ProcessListView, self).__init__(parent)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)

    def contextMenuEvent(self, event):
        """define context menu within list view
        - add
        - edit
        - delete"""
        local_position = event.pos()
        global_position = event.globalPos()
        item = self.indexAt(local_position)
        print(item)
        context_menu = QMenu()
        if item.isValid():
            edit_action = context_menu.addAction("Edit")
            edit_action.triggered.connect(lambda: self.edit_add.emit("Edit", item, self.model()))
            delete_action = context_menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self.model().removeRow(item.row()))
        add_action = context_menu.addAction("Add")
        add_action.triggered.connect(lambda: self.edit_add.emit("Add", QModelIndex(), self.model()))

        context_menu.exec_(global_position)


class ListModel(QAbstractListModel):
    """define model for variables list views"""

    def __init__(self, data={}):
        super(ListModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def data(self, index, role=None):
        key = list(self._data.keys())[index.row()]

        if role == Qt.DisplayRole:
            return key
        elif role == Qt.EditRole:
            return key
        #return QVariant()

    def setData(self, index, value, role=None):
        key = list(self._data.keys())[index.row()]
        self._data[key] = value
        print("setData")
        print(self._data)
        self.dataChanged.emit()
        return True

    def addData(self, index, value):
        pass

    def removeRow(self, row, parent=None, *args, **kwargs):
        key = list(self._data.keys())[row]
        del self._data[key]
        print("removeRow")
        print(self._data)
        self.dataChanged.emit()
        return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsAutoTristate
