from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import osdria_app_rc


class SectionSelector(QLabel):
    """hover effect over different sections of logo
    and navigation to respective page"""
    clicked = Signal(str)
    hovered = Signal(str)

    def __init__(self, parent):
        super(SectionSelector, self).__init__(parent)
        self._section = "Overview"
        self.loadLogos()

    def resetLogo(self):
        self.section = "Overview"

    def loadLogos(self):
        self.image = {
            "Overview": QPixmap(":/icons/img/logo_light@2x.png"),
            "Energy": QPixmap(":/icons/img/logo_light_energy@2x.png"),
            "Water": QPixmap(":/icons/img/logo_light_water@2x.png"),
            "Food": QPixmap(":/icons/img/logo_light_food@2x.png"),
            "Business": QPixmap(":/icons/img/logo_light_business@2x.png")
        }

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        print("section change")
        if value in self.image.keys():
            self._section = value
            self.setPixmap(self.image[self.section])

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
        elif waterX & waterY:
            self.section = "Water"
        elif foodX & foodY:
            self.section = "Food"
        elif businessX & businessY:
            self.section = "Business"
        else:
            self.section = "Overview"

        # emit hovered signal to change title
        self.hovered.emit(self.section)

    def mousePressEvent(self, event):
        """emit clicked signal with corresponding section"""
        if self._section is not "Overview":
            self.clicked.emit(self.section)

    def resizeEvent(self, event):
        print("resizeEvent()")
        """keep aspect ratio of logo"""
        width = self.width()
        height = self.height()
        posX = (self.parent().width() - width) / 2
        posY = (self.parent().height() - height) / 2
        minSize = min(width, height)
        self.setGeometry(posX, posY, minSize, minSize)
