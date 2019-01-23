from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import appColors as col
import appTexts as txt
import appIcons as icn


SCREEN_HEIGHT_RATIO = 2
FILE_EXTENSION = "OSCAR files (*.pdf)"


class WelcomeScreen(QDialog):
    """Creation of the Welcome Screen
    includes interaction for creating new file
    as well as opening existing file
    """
    newProject = True
    filename = ""
    leftClick = False

    def __init__(self):
        super().__init__(None, Qt.FramelessWindowHint)
        self.initUi()

    def initUi(self):
        # define dialog design
        self.sizeScreen()

        # create content
        self.closeButton = QPushButton(self)
        closeIcon = QPixmap(icn.close['normal'])
        self.closeButton.setIcon(closeIcon)
        self.closeButton.setFixedSize(closeIcon.rect().size())
        self.closeButton.setFlat(True)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(icn.logo))
        self.welcomeText = QLabel(txt.WELCOME)
        self.createButton = ProjectButton(self, icn.new, txt.CREATE_PROJECT)
        self.openButton = ProjectButton(self, icn.open, txt.OPEN_PROJECT)

        # define content structure
        self.structureContent()

        # bind buttons to functions
        self.closeButton.clicked.connect(self.reject)
        self.createButton.clicked.connect(self.newDialog)
        self.openButton.clicked.connect(self.openDialog)

    def newDialog(self):
        self.dialog = QFileDialog(self, txt.CREATE_PROJECT['sub'])
        self.dialog.setAcceptMode(QFileDialog.AcceptSave)
        self.dialog.accepted.connect(self.closeNewDialog)
        self.dialog.open()

    def closeNewDialog(self):
        self.filename = self.dialog.selectedFiles()[0]
        self.accept()

    def openDialog(self):
        self.dialog = QFileDialog(self, txt.OPEN_PROJECT['sub'])
        self.dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.dialog.setNameFilter(FILE_EXTENSION)
        self.dialog.accepted.connect(self.closeOpenDialog)
        self.dialog.open()

    def closeOpenDialog(self):
        self.filename = self.dialog.selectedFiles()[0]
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
        vSizer = QVBoxLayout()
        vSizer.addSpacing(10)
        vSizer.addWidget(self.logo, 0, Qt.AlignCenter)
        vSizer.addWidget(self.welcomeText, 0, Qt.AlignCenter)
        vSizer.addWidget(self.createButton, 0, Qt.AlignLeft)
        vSizer.addWidget(self.openButton, 0, Qt.AlignLeft)

        # align horizontally centered
        hSizer = QHBoxLayout()
        hSizer.addStretch()
        hSizer.addLayout(vSizer)
        hSizer.addStretch()

        # align vertically, close button above
        topVSizer = QVBoxLayout(self)
        topVSizer.addWidget(self.closeButton, 0, Qt.AlignLeft)
        topVSizer.addLayout(hSizer)
        self.setLayout(topVSizer)

    def mousePressEvent(self, event):
        if event.button() is Qt.LeftButton:
            self.relativeCursorPosition = self.pos() - event.globalPos()
            self.leftClick = True

    def mouseReleaseEvent(self, event):
        if event.button() is Qt.LeftButton:
            self.leftClick = False

    def mouseMoveEvent(self, event):
        """move dialog with mouse clicked move"""
        if self.leftClick:
            self.move(event.globalPos() + self.relativeCursorPosition)


class ProjectButton(QWidget):
    """Entry level project buttons
    including icon, title and subtext"""
    clicked = Signal()
    hovered = Signal()

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

    def onPaint():
        option = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_FrameFocusRect,
                                   option,
                                   painter,
                                   self)
