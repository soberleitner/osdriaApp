import sys
import appIcons as icn
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from welcomeScreen import WelcomeScreen

FILE_EXTENSION = "OSCAR files (*.pdf)"


class osdriaApp():
    """top-level class of app"""
    def __init__(self):
        # setting high DPI support
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # load icons from files
        icn.init()

        osdria = QApplication([])

        # create welcomeDialog
        welcomeDialog = WelcomeScreen()
        if not welcomeDialog.exec_():
            sys.exit(-1)

        print(welcomeDialog.filename)
        # ProjectScreen(file=welcomeDialog.filename[0], new=welcomeDialog.newProject)

        sys.exit(osdria.exec_())


if __name__ == '__main__':
    osdriaApp()
