from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLineEdit


class PropertyEdit(QLineEdit):
    """custom QLineEdit class for click-able actions
    @signal: clicked()
    @signal: inputFinished(str)"""
    clicked = Signal()
    inputFinished = Signal(str)

    def __init__(self, parent):
        super(PropertyEdit, self).__init__(parent)
        self.returnPressed.connect(self.clearFocus)
        self._unit = ""

    def setText(self, value):
        print("setText")
        self.add_unit(value)

    def set_unit(self, unit):
        print("set_unit")
        self._unit = unit

    def text(self):
        print("text")
        if self._unit is "":
            return super().text()
        else:
            # remove unit
            return super().text().split(" " + self._unit)[0]

    def mousePressEvent(self, event):
        print("mousePressEvent")
        super().setText(self.text())
        self.clicked.emit()

    def focusOutEvent(self, event):
        print("focusOutEvent")
        # add unit
        self.add_unit(super().text())

        super().focusOutEvent(event)
        if self.hasAcceptableInput():
            self.inputFinished.emit(self.text())

    def add_unit(self, value):
        displayed_text = value
        if self._unit is not "":
            displayed_text += " " + self._unit
        super().setText(displayed_text)
