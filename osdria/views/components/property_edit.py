from PySide2.QtCore import Signal, QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QLineEdit


class PropertyEdit(QLineEdit):
    """custom QLineEdit class for click-able actions
    @signal: clicked()
    @signal: inputFinished(str)"""
    clicked = Signal()
    inputFinished = Signal(str)

    def __init__(self, parent):
        super(PropertyEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.returnPressed.connect(self.clearFocus)
        self._unit = ""
        self._popup = False

    def setText(self, value):
        self.add_unit(value)

    def set_unit(self, unit):
        self._unit = unit

    def text(self):
        if self._unit is "":
            return super().text()
        else:
            # remove unit
            return super().text().split(" " + self._unit)[0]

    def is_popup(self):
        return self._popup

    def set_popup(self, value):
        self._popup = value
        dropdown_icon = QIcon()
        dropdown_icon.addPixmap(QPixmap(":/icons/img/dropdown_normal@2x.png"), QIcon.Normal, QIcon.Off)
        dropdown_icon.actualSize(QSize(10, 10))
        popup_action = self.addAction(dropdown_icon, QLineEdit.TrailingPosition)
        popup_action.triggered.connect(self.clicked.emit)

    def mousePressEvent(self, event):
        super().setText(self.text())
        if self.isReadOnly():
            self.clicked.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        # add unit
        self.add_unit(super().text())

        if self.hasAcceptableInput():
            self.inputFinished.emit(self.text())

    def add_unit(self, value):
        """adding unit to displayed text"""
        displayed_text = str(value)
        if self._unit is not "":
            displayed_text += " " + self._unit
        super().setText(displayed_text)
