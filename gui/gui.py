import sys
import appIcons as icn
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from welcomeScreen import WelcomeScreen


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

        # load icons from files
        icn.init()

        osdria = QApplication([])
        osdria.setStyleSheet(style)

        # display welcomeDialog
        welcomeDialog = WelcomeScreen()
        if not welcomeDialog.exec_():
            sys.exit(0)

        print(welcomeDialog.filename)
        # ProjectScreen(file=welcomeDialog.filename, new=welcomeDialog.newProject)

        sys.exit(osdria.exec_())


if __name__ == '__main__':
    osdriaApp()
