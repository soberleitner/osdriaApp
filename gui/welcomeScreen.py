from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import appColors as col
import appTexts as txt
import appIcons as icn


SCREEN_HEIGHT_RATIO = 2


class WelcomeScreen(QDialog):
    """Creation of the Welcome Screen
    includes interaction for creating new file
    as well as opening existing file
    """
    newProject = True
    filename = ""

    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        # define frame design
        self.sizeScreen()

        # create content
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(icn.logo))
        self.welcomeText = QLabel(txt.WELCOME)
        self.createButton = ProjectButton(self, icn.new, txt.CREATE_PROJECT)
        self.openButton = ProjectButton(self, icn.open, txt.OPEN_PROJECT)

        # define content structure
        self.structureContent()

        # bind buttons to functions
        self.createButton.clicked.connect(self.newDialog)
        self.openButton.clicked.connect(self.openDialog)

    def newDialog(self):
        self.filename = QFileDialog.getSaveFileName(
            self,
            txt.CREATE_PROJECT['sub'])
        self.accept()

    def openDialog(self):
        self.filename = QFileDialog.getSaveFileName(
            self,
            txt.CREATE_PROJECT['sub'],
            ".",
            FILE_EXTENSION)
        self.newProject = False
        self.accept()

    def sizeScreen(self):
        """define size and location of screen"""
        desktopRect = QDesktopWidget().availableGeometry()
        screenHeight = desktopRect.height() / SCREEN_HEIGHT_RATIO
        screenCenter = desktopRect.center()
        screenRect = QRect(0, 0, screenHeight, screenHeight)
        screenRect.moveCenter(screenCenter)

        self.setGeometry(screenRect)

    def structureContent(self):
        """define structure of contents"""
        verticalSizer = QVBoxLayout()
        verticalSizer.addSpacing(10)
        verticalSizer.addWidget(self.logo, 0, Qt.AlignCenter)
        verticalSizer.addWidget(self.welcomeText, 0, Qt.AlignCenter)
        verticalSizer.addWidget(self.createButton, 0, Qt.AlignLeft)
        verticalSizer.addWidget(self.openButton, 0, Qt.AlignLeft)

        # align horizontally centered
        horizontalSizer = QHBoxLayout(self)
        horizontalSizer.addStretch()
        horizontalSizer.addLayout(verticalSizer)
        horizontalSizer.addStretch()
        self.setLayout(horizontalSizer)


class ProjectButton(QWidget):
    """Entry level project buttons
    including icon, title and subtext"""
    clicked = Signal()

    def __init__(self, parent, icon, text):
        super(ProjectButton, self).__init__(parent)
        self.icon = QLabel(self)
        self.icon.setPixmap(QPixmap(icon))
        self.title = QLabel(text['main'])
        self.sub = QLabel(text['sub'])

        # vertical sizer for title and subtext
        verticalSizer = QVBoxLayout()
        verticalSizer.addWidget(self.title, 0, Qt.AlignLeft)
        verticalSizer.addWidget(self.sub, 0, Qt.AlignLeft)

        # horizontal sizer for icon and text
        horizontalSizer = QHBoxLayout(self)
        horizontalSizer.addWidget(self.icon, 0, Qt.AlignCenter)
        horizontalSizer.addLayout(verticalSizer)
        self.setLayout(horizontalSizer)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.unsetCursor()
