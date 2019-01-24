from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import appColors as col
import appTexts as txt
import appIcons as icn


SCREEN_SIZE = 450
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
        super().__init__(None, Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.initUi()

    def initUi(self):
        # define dialog design
        self.sizeScreen()

        # create content
        self.frame = QFrame(self)
        self.closeButton = QPushButton(self.frame)
        self.closeButton.setIcon(icn.close)
        self.closeButton.setFlat(True)
        self.closeButton.setChecked(True)

        self.logo = QLabel(self.frame)
        self.logo.setPixmap(icn.logo)
        self.welcomeText = QLabel(txt.WELCOME)
        self.createButton = ProjectButton(self.frame, icn.new, txt.CREATE_PROJECT)
        self.openButton = ProjectButton(self.frame, icn.open, txt.OPEN_PROJECT)

        # define content structure
        self.structureContent()

        # bind buttons to functions
        self.closeButton.clicked.connect(self.reject)
        self.createButton.clicked.connect(self.newDialog)
        self.openButton.clicked.connect(self.openDialog)

    def newDialog(self):
        self.dialog = QFileDialog(self.frame, txt.CREATE_PROJECT['sub'])
        self.dialog.setAcceptMode(QFileDialog.AcceptSave)
        self.dialog.accepted.connect(self.closeNewDialog)
        self.dialog.open()

    def closeNewDialog(self):
        self.filename = self.dialog.selectedFiles()[0]
        self.accept()

    def openDialog(self):
        self.dialog = QFileDialog(self.frame, txt.OPEN_PROJECT['sub'])
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
        screenCenter = QDesktopWidget().availableGeometry().center()
        screenRect = QRect(0, 0, SCREEN_SIZE, SCREEN_SIZE)
        screenRect.moveCenter(screenCenter)

        self.setGeometry(screenRect)

    def structureContent(self):
        """define structure of contents"""
        vSizer = QVBoxLayout()
        vSizer.setMargin(0)
        vSizer.setSpacing(0)
        vSizer.addWidget(self.logo, 0, Qt.AlignCenter)
        vSizer.addWidget(self.welcomeText, 0, Qt.AlignCenter)
        vSizer.addWidget(self.createButton, 0, Qt.AlignLeft)
        vSizer.addWidget(self.openButton, 0, Qt.AlignLeft)

        # align horizontally centered
        hSizer = QHBoxLayout()
        hSizer.setMargin(0)
        hSizer.setSpacing(0)
        hSizer.addStretch()
        hSizer.addLayout(vSizer)
        hSizer.addStretch()

        # align vertically, close button above
        topVSizer = QVBoxLayout(self.frame)
        topVSizer.setMargin(0)
        topVSizer.addWidget(self.closeButton, 0, Qt.AlignLeft)
        topVSizer.addLayout(hSizer)
        self.frame.setLayout(topVSizer)

        topSizer = QHBoxLayout(self)
        topSizer.addWidget(self.frame)
        self.setLayout(topSizer)

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
    MAIN_TEXT_HEIGHT = 17
    SUB_TEXT_HEIGHT = 13

    clicked = Signal()
    hovered = Signal()

    def __init__(self, parent, icon, text):
        super(ProjectButton, self).__init__(parent)
        self.icon = QLabel(self)
        self.icon.setPixmap(icon)
        self.title = QLabel(text['main'])
        self.title.setFixedHeight(self.MAIN_TEXT_HEIGHT)
        self.title.setProperty("type", "main")
        self.sub = QLabel(text['sub'])
        self.sub.setFixedHeight(self.SUB_TEXT_HEIGHT)
        self.sub.setProperty("type", "sub")

        # vertical sizer for title and subtext
        verticalSizer = QVBoxLayout()
        verticalSizer.setMargin(0)
        verticalSizer.setSpacing(0)
        verticalSizer.setContentsMargins(0, 0, 0, 0)
        verticalSizer.addWidget(self.title, 0, Qt.AlignLeft)
        verticalSizer.addWidget(self.sub, 0, Qt.AlignLeft)

        # horizontal sizer for icon and text
        horizontalSizer = QHBoxLayout(self)
        horizontalSizer.setMargin(0)
        horizontalSizer.setSpacing(0)
        horizontalSizer.addWidget(self.icon, 0, Qt.AlignLeft)
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
