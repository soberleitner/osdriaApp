from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import appTexts as txt
import appIcons as icn


class Toolbar(QFrame):
    """custom toolbar with specficied spaces"""

    def __init__(self, parent):
        super(Toolbar, self).__init__(parent)

        # initialize size
        self.setFixedHeight(50)
        self.setFixedWidth(parent.width())
        
        #initialize structure
        self.horizontalLayout = QHBoxLayout(self)
        self.setLayout(self.horizontalLayout)
        self.toBase()

    def initSize(self):
        

    def initElements(self):
        # initialization not possible this way, will appear at the toolbar because of parent setting
        self.label = QLabel(self)
        #self.label.setFixedHeight(50)
        self.empty = ToolButton(self, "empty")
        self.dropdown = QComboBox(self)

        for icon in icn.ICON_BUTTON_LIST:
            vars(self)[icon] = ToolButton(self, vars(icn)[icon])
        for icon in icn.ICON_TOGGLE_LIST:
            vars(self)[icon] = ToolButton(self, vars(icn)[icon])

    def initStructure(self):
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

        self.topLayout = QHBoxLayout(self)
        self.topLayout.setMargin(0)
        self.topLayout.setSpacing(0)
        self.topLayout.addLayout(leftLayout)
        self.topLayout.addWidget(self.label, 0, Qt.AlignHCenter)
        self.topLayout.addLayout(rightLayout)
        self.setLayout(self.topLayout)

    def toBase(self):
        # new intialisation
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

    def onPaint():
        option = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_FrameFocusRect,
                                   option,
                                   painter,
                                   self)


class ToolButton(QToolButton):
    """custom toolbar button"""
    def __init__(self, parent, icon):
        super(ToolButton, self).__init__(parent)

        if icon is "empty":
            self.setIcon(icn.trash)
        else:
            self.setIcon(icon)
        # self.setFixedSize(50, 50)
        # self.setContentsMargins(0, 0, 0, 0)

    def enterEvent(self, event):
        print("enter")
        self.setIcon(QIcon(self.icon().pixmap(QSize(100, 100), QIcon.Active)))

    def leaveEvent(self, event):
        print("leave")
        self.setIcon(QIcon(self.icon().pixmap(QSize(100, 100), QIcon.Normal)))
