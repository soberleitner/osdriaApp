from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

from ui import welcomeDialog
import appTexts as txt
import appColors as col

FILE_EXTENSION = "OSCAR files (*.pdf)"


class WelcomeScreen(welcomeDialog.Ui_Dialog, QDialog):
    """Creation of the Welcome Screen
    includes interaction for creating new file
    as well as opening existing file
    """
    def __init__(self):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super().__init__(None, settings)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setupUi(self)

        # bind actions
        self.actionNew.triggered.connect(self.newDialog)
        self.actionOpen.triggered.connect(self.openDialog)
        self.frameCreate.clicked.connect(self.newDialog)
        self.frameOpen.clicked.connect(self.openDialog)

    def newDialog(self):
        self.dialog = QFileDialog(self.welcomeFrame, txt.CREATE_PROJECT['sub'])
        self.dialog.setAcceptMode(QFileDialog.AcceptSave)
        self.dialog.accepted.connect(self.closeNewDialog)
        self.dialog.open()

    def closeNewDialog(self):
        self.filename = self.dialog.selectedFiles()[0]
        self.newProject = True
        self.accept()

    def openDialog(self):
        self.dialog = QFileDialog(self.welcomeFrame, txt.OPEN_PROJECT['sub'])
        self.dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.dialog.setNameFilter(FILE_EXTENSION)
        self.dialog.accepted.connect(self.closeOpenDialog)
        self.dialog.open()

    def closeOpenDialog(self):
        self.filename = self.dialog.selectedFiles()[0]
        self.newProject = False
        self.accept()

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
