from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class ToolButton(QToolButton):
    """define functionality of tool button
    with hover effect"""
    def __init__(self, parent):
        super(ToolButton, self).__init__(parent)

    def enterEvent(self, event):
        self.setEnabled(True)

    def leaveEvent(self, event):
        self.setEnabled(False)
