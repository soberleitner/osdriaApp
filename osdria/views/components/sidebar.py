from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

SIDEBAR_WIDTH = 260

PROP_TYPE_TEXT = 0
PROP_TYPE_DIALOG = 1
PROP_TYPE_POPUP = 2
PROP_TYPE_DRAFT = 3


class Sidebar(QListWidget):
    """custom sidebar widget for displaying properties & draft elements"""
    def __init__(self, parent):
        super(Sidebar, self).__init__(parent)

    def toggle(self, button):
        """show or hide sidebar"""
        width = self.geometry().width()
        self.setMaximumWidth(SIDEBAR_WIDTH - width)

    def loadData(self, dataList):
        """retrieve data to display properties"""
        for data in dataList:
            item = PropertyWidget(self, data)
            itemWidget = QListWidgetItem(self)
            itemWidget.setSizeHint(item.sizeHint())
            self.addItem(itemWidget)
            self.setItemWidget(itemWidget, item)


class PropertyWidget(QWidget):
    """custom list item to view properties in sidebar"""
    def __init__(self, parent, data):
        super(PropertyWidget, self).__init__(parent)
        self.name = data["name"]
        self.value = data["value"]
        self.type = data["type"]
        if self.type is PROP_TYPE_DIALOG:
            self.dialog = data["dialog"]
        elif self.type is PROP_TYPE_POPUP:
            self.popup = data["popup"]
        self.initUi()

    def initUi(self):
        """set up the layout of property name above property entry
        differentiate between QLineEdit, QPushButton, QComboBox as entry"""
        propertyLabel = QLabel(self.name)
        if self.type is PROP_TYPE_TEXT:
            self.propertyEntry = QLineEdit(self.value)
        elif self.type is PROP_TYPE_DIALOG:
            self.propertyEntry = QPushButton(self.value)
            self.propertyEntry.clicked.connect(self.openDialog)

        verticalLayout = QVBoxLayout(self)
        verticalLayout.setSpacing(5)
        verticalLayout.setContentsMargins(11, 5, 11, 5)
        verticalLayout.addWidget(propertyLabel)
        verticalLayout.addWidget(self.propertyEntry)
        self.setLayout(verticalLayout)

    def openDialog(self):
        """dialog for QPushButton"""
        location = QInputDialog.getDouble(
            self,
            "Enter location",
            "Location:",
            100)
        self.propertyEntry.setText(str(location))
