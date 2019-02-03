from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

"""linkage between button states & modes and QIcon image type:
isEnabled | isChecked |     image type      | toggle colour | button colour
    0           0       not available, off      grey            grey
    0           1       available, on           orange          white
    1           0       normal, off             orange
    1           1       normal, on              grey
"""


class ToolButton(QToolButton):
    """define functionality of tool button
    with hover effect"""
    clicked = Signal(QToolButton)

    def __init__(self, parent):
        super(ToolButton, self).__init__(parent)
        self.select = self.isChecked()

    def enterEvent(self, event):
        self.setEnabled(True)

    def leaveEvent(self, event):
        if self.select:
            self.setChecked(not self.isChecked())
            self.select = False
        self.setEnabled(False)

    def mousePressEvent(self, event):
        # toggle select mode when button is checkable
        if self.isCheckable():
            self.select = True

        self.clicked.emit(self)
