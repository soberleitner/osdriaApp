import sys
import appIcons as icn
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from welcomeScreen import WelcomeScreen
from projectScreen import ProjectScreen


class osdriaApp():
    """top-level class of app"""
    def __init__(self):
        # setting high DPI support
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # load stylesheet
        styleFile = QFile('style.css')
        styleFile.open(QFile.ReadOnly)
        style = str(styleFile.readAll())

        osdria = QApplication([])
        osdria.setStyleSheet(style)

        # load icons from files
        icn.init()

        # display welcomeDialog
        welcomeDialog = WelcomeScreen()
        if not welcomeDialog.exec_():
            sys.exit(0)

        projectScreen = ProjectScreen(welcomeDialog.newProject)
        projectScreen.show()

        sys.exit(osdria.exec_())


if __name__ == '__main__':
    osdriaApp()
