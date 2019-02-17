from PySide2.QtWidgets import *
from PySide2.QtGui import QFont
from PySide2.QtCore import QPoint


class PropertyPopupView(QMenu):
    """view of property popup"""

    def __init__(self, parent, popup_model, popup_controller):
        super(PropertyPopupView, self).__init__(parent)
        self._model = popup_model
        self._popup_ctrl = popup_controller

        """connect widgets to controller"""
        self.triggered.connect(self._popup_ctrl.set_popup_value)

        """initialise view"""
        for index, choice in enumerate(self._model.choices[1:]):
            # create and add action with name of choice and index
            # without first element
            popup_action = QAction(choice.name, self.parent())
            popup_action.setData(index + 1)
            self.addAction(popup_action)
        self.setFont(self.parent().font())

    def show_popup(self):
        """override popup function"""
        height = self.parent().height()
        position = self.parent().mapToGlobal(QPoint(0, height + 5))
        self.popup(position)

