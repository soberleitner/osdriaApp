from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from views.project_view_ui import Ui_MainWindow
import views.components.sidebar as sidebar


sidebarDataOverview = [
    {
        "name": "Project Name",
        "value": "Nsutam",
        "type": sidebar.PROP_TYPE_TEXT
    },
    {
        "name": "Project Location",
        "value": "6.98, -1.91",
        "type": sidebar.PROP_TYPE_DIALOG,
        "dialog": "location"
    },
    {
        "name": "Project Area",
        "value": "120.0 ha",
        "type": sidebar.PROP_TYPE_TEXT
    }]


class ProjectView(QMainWindow):
    """Main Project window"""
    def __init__(self, filename, newProject=True):
        super(ProjectView, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.titleOverview.setText("Overview")
        self._ui.logo.resetLogo()

        # bind data source
        self._ui.sidebarOverview.loadData(sidebarDataOverview)

        # bind actions
        self._ui.logo.hovered.connect(self._ui.titleOverview.setText)

        self._ui.logo.clicked.connect(self.toSectionsPage)
        self._ui.toolDraft.clicked.connect(self.toDraftPage)
        self._ui.toolGraph.clicked.connect(self.toGraphPage)
        self._ui.toolBackSections.clicked.connect(self.toBackPage)
        self._ui.toolBackDraft.clicked.connect(self.toBackPage)
        self._ui.toolBackGraph.clicked.connect(self.toBackPage)

        self._ui.toolSidebarOverview.clicked.connect(self._ui.sidebarOverview.toggle)
        self._ui.toolSidebarSections.clicked.connect(self._ui.sidebarSections.toggle)
        self._ui.toolSidebarDraft.clicked.connect(self._ui.sidebarDraft.toggle)
        self._ui.toolBackDraft.clicked.connect(self._ui.draftbar.toggle)
        self._ui.toolDraft.clicked.connect(self._ui.draftbar.toggle)

    def toSectionsPage(self, section):
        """prepare for switch to sections page"""
        self._ui.titleSections.setText(section)
        self._ui.stackedPages.setCurrentIndex(1)

    def toDraftPage(self):
        """prepare for switch to draft page"""
        self._ui.titleDraft.setText(str(self._ui.titleSections.text()) + " - Draft")
        self._ui.stackedPages.setCurrentIndex(2)

    def toGraphPage(self):
        """prepare for switch to graph page"""
        self._ui.titleGraph.setText(self._ui.titleSections.text())
        self._ui.stackedPages.setCurrentIndex(3)

    def toBackPage(self, senderButton):
        """define stackedPages index of back buttons"""
        pageBackCount = 1
        if senderButton is self._ui.toolBackGraph:
            pageBackCount += 1

        newStackedPagesIndex = self._ui.stackedPages.currentIndex() - pageBackCount
        self._ui.stackedPages.setCurrentIndex(newStackedPagesIndex)
