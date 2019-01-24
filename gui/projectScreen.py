from PySide2.QtCore import *
from PySide2.QtWidgets import *

import appIcons as icn

from toolbar import Toolbar


class ProjectScreen(QMainWindow):
    """Main Project window"""
    def __init__(self, filename, newProject=True):
        super(ProjectScreen, self).__init__()

        self.initUi()

    def initUi(self):
        self.setWindowState(Qt.WindowFullScreen)
        self.toolbar = Toolbar(self)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout.addWidget(self.toolbar, 1, Qt.AlignTop)
        self.setLayout(self.verticalLayout)

    def resizeEvent(self, event):
        self.toolbar.setFixedWidth(self.width())