from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import icons_rc


class SectionSelector(QLabel):
    """hover effect over different sections of logo
    and navigation to respective page"""
    clicked = Signal(str)
    hovered = Signal(str)

    def __init__(self, parent):
        super(SectionSelector, self).__init__(parent)

    def mouseMoveEvent(self, event):
        """set section variable according to mouse position"""
        relativeX = event.pos().x() / self.width()
        relativeY = event.pos().y() / self.height()

        # check conditions for all four section regions
        energyX = (relativeX > 50 / 1800) & (relativeX < 570 / 1800)
        energyY = (relativeY > 950 / 1800) & (relativeY < 1500 / 1800)
        waterX = (relativeX > 700 / 1800) & (relativeX < 1100 / 1800)
        waterY = (relativeY > 0 / 1800) & (relativeY < 500 / 1800)
        foodX = (relativeX > 1230 / 1800) & (relativeX < 1750 / 1800)
        foodY = (relativeY > 950 / 1800) & (relativeY < 1500 / 1800)
        businessX = (relativeX > 570 / 1800) & (relativeX < 1230 / 1800)
        businessY = (relativeY > 600 / 1800) & (relativeY < 1200 / 1800)

        # perform hovering effect for the corresponding section
        if energyX & energyY:
            self.section = "Energy"
            self.setPixmap(":/icons/icons/logo_light_energy@2x.png")
        elif waterX & waterY:
            self.section = "Water"
            self.setPixmap(":/icons/icons/logo_light_water@2x.png")
        elif foodX & foodY:
            self.section = "Food"
            self.setPixmap(":/icons/icons/logo_light_food@2x.png")
        elif businessX & businessY:
            self.section = "Business"
            self.setPixmap(":/icons/icons/logo_light_business@2x.png")
        else:
            self.section = "Overview"
            self.setPixmap(":/icons/icons/logo_light@2x.png")

        # emit hovered signal to change title
        self.hovered.emit(self.section)

    def mousePressEvent(self, event):
        """emit clicked signal with corresponding section"""
        if self.section is not "Overview":
            self.clicked.emit(self.section)

    # def resizeEvent(self):
    #     print("resize")
    #     pixmap = self.pixmap()
    #     width = self.width()
    #     height = self.height()

    #     self.setPixmap(pixmap.scaled(width, height, Qt.KeepAspectRatio))
