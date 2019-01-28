from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui import main


class ProjectScreen(main.Ui_MainWindow, QMainWindow):
    """Main Project window"""
    def __init__(self, filename, newProject=True):
        super(ProjectScreen, self).__init__()
        self.setupUi(self)

        # bind actions
        self.logo.hovered.connect(self.changeTitle)
        self.logo.clicked.connect(self.changePageToSections)
        self.toolBackSections.clicked.connect(self.changePageToOverview)
        self.toolGraph.clicked.connect(self.changePageToGraph)
        self.toolDraft.clicked.connect(self.changePageToDraft)
        self.toolBackDraft.clicked.connect(self.changePageToSections)
        self.toolBackGraph.clicked.connect(self.changePageToSections)

    def changeTitle(self, sectionName="Overview"):
        self.titleOverview.setText(sectionName)

    def changePageToOverview(self):
        self.stackedPages.setCurrentIndex(0)

    def changePageToSections(self, section):
        self.stackedPages.setCurrentIndex(1)
        self.titleSections.setText(section)

    def changePageToDraft(self):
        self.stackedPages.setCurrentIndex(2)

    def changePageToGraph(self):
        self.stackedPages.setCurrentIndex(3)
