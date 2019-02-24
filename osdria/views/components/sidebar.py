from PySide2.QtCore import Signal
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from models.property import *
from controllers.property_ctrl import PropertyCtrl
from views.property_view import PropertyView

SIDEBAR_WIDTH = 260


class Sidebar(QListWidget):
    """custom sidebar widget for displaying properties & draft elements"""
    def __init__(self, parent):
        super(Sidebar, self).__init__(parent)

    def toggle(self):
        """show or hide sidebar"""
        width = self.geometry().width()
        self.setMaximumWidth(SIDEBAR_WIDTH - width)

    def load_data(self, property_list):
        """retrieve data to display properties"""
        self.clear()
        for _, prop in property_list.items():
            property_ctrl = PropertyCtrl(prop)
            item = PropertyView(self, prop, property_ctrl)
            item_widget = QListWidgetItem(self)
            item_widget.setSizeHint(item.sizeHint())
            self.addItem(item_widget)
            self.setItemWidget(item_widget, item)
