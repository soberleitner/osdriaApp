from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import appTexts as txt
import appIcons as icn

class Toolbar(QWidget):
    """custom toolbar with specficied spaces"""

    def __init__(self, parent):
        super(Toolbar, self).__init__(parent)
        self.parent = parent

        self.initSize()
        self.initElements()
        self.toBase()
        self.initStructure()

    def initSize(self):
        self.setFixedHeight(50)
        self.setFixedWidth(self.parent.width())

    def initElements(self):
        print("initElements")
        self.label = QLabel(self)
        self.empty = ToolButton(self, "empty")
        self.dropdown = QComboBox(self)

        for icon in icn.ICON_BUTTON_LIST:
            vars(self)[icon] = ToolButton(self, vars(icn)[icon])
        for icon in icn.ICON_TOGGLE_LIST:
            vars(self)[icon] = ToolButton(self, vars(icn)[icon])

    def initStructure(self):
        print("initStructure")
        leftLayout = QHBoxLayout()
        leftLayout.addWidget(self.tools[1])
        leftLayout.addWidget(self.tools[2])
        leftLayout.addSpacing(200)
        leftLayout.addWidget(self.tools[3])
        leftLayout.addWidget(self.tools[4])
        leftLayout.addWidget(self.tools[5])
        leftLayout.addStretch()

        rightLayout = QHBoxLayout()
        rightLayout.addWidget(self.tools[6])
        rightLayout.addWidget(self.tools[7])
        rightLayout.addWidget(self.tools[8])
        rightLayout.addWidget(self.tools[9])
        rightLayout.addWidget(self.tools[10])

        topLayout = QHBoxLayout(self)
        topLayout.addLayout(leftLayout)
        topLayout.addWidget(self.label, 0, Qt.AlignHCenter)
        topLayout.addLayout(rightLayout)
        self.setLayout(topLayout)

    def toBase(self):
        print("toBase")
        self.label.setText(txt.SECTIONS['over'])
        self.tools = [
            self.empty,
            self.empty,
            self.scenarios,
            self.dropdown,
            self.run,
            self.export,
            self.empty,
            self.empty,
            self.empty,
            self.empty,
            self.sidebar
        ]

    def toSector():
        pass


class ToolButton(QToolButton):
    """custom toolbar button"""
    def __init__(self, parent, icon):
        super(ToolButton, self).__init__(parent)

        if icon is "empty":
            self.setIcon(QIcon(QPixmap(50, 50)))
        else:
            self.setIcon(icon)
        self.setFixedSize(50, 50)

    def enterEvent(self, event):
        print("enter")
        self.setIcon(QIcon(self.icon().pixmap(QSize(30, 30), QIcon.Active)))

    def leaveEvent(self, event):
        print("leave")
        self.setIcon(QIcon(self.icon().pixmap(QSize(30, 30), QIcon.Normal)))
