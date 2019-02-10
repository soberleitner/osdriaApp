from PySide2.QtCore import Signal
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from models.constants import PropType
from models.property import Property

SIDEBAR_WIDTH = 260


class Sidebar(QListWidget):
    """custom sidebar widget for displaying properties & draft elements"""
    item_clicked = Signal(Property)

    def __init__(self, parent):
        super(Sidebar, self).__init__(parent)

    def toggle(self):
        """show or hide sidebar"""
        width = self.geometry().width()
        self.setMaximumWidth(SIDEBAR_WIDTH - width)

    def load_data(self, data_list):
        """retrieve data to display properties"""
        for data in data_list:
            item = PropertyWidget(self, data)
            item_widget = QListWidgetItem(self)
            item_widget.setSizeHint(item.sizeHint())
            self.addItem(item_widget)
            self.setItemWidget(item_widget, item)

    def clicked(self, prop):
        self.item_clicked.emit(prop)


class PropertyWidget(QWidget):
    """custom list item to view properties in sidebar"""

    def __init__(self, parent, data):
        super(PropertyWidget, self).__init__(parent)
        self._name = data.name
        self._value = data.value
        self._type = data.prop_type

        self.init_ui()

    def init_ui(self):
        """set up the layout of property name above property entry
        differentiate between QLineEdit, QPushButton, QComboBox as entry"""
        property_label = QLabel(self._name)
        if self._type is PropType.LINE_EDIT:
            self.property_entry = QLineEdit(self._value)
        elif self._type is PropType.DIALOG:
            self.property_entry = QPushButton(self._value)
            self.property_entry.clicked.connect(self.open_dialog)

        vertical_layout = QVBoxLayout(self)
        vertical_layout.setSpacing(5)
        vertical_layout.setContentsMargins(11, 5, 11, 5)
        vertical_layout.addWidget(property_label)
        vertical_layout.addWidget(self.property_entry)
        self.setLayout(vertical_layout)

    def open_dialog(self):
        """dialog for QPushButton"""
        location = QInputDialog.getDouble(
            self,
            "Enter location",
            "Location:",
            100)
        self.property_entry.setText(str(location))
