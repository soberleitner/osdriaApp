from PySide2.QtWidgets import *

from models.property import *
from models.constants import PropType
from views.property_view_ui import Ui_property


class PropertyView(QWidget):
    """view of property in sidebar"""

    def __init__(self, parent, property_model, property_controller):
        super(PropertyView, self).__init__(parent)

        self._model = property_model
        self._property_ctrl = property_controller
        self._ui = Ui_property()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        if self._model.type is PropType.LINE_EDIT:
            self._ui.property_value.inputFinished.connect(
                self._property_ctrl.change_property_value)
        elif self._model.type is PropType.DIALOG:
            self._ui.property_value.clicked.connect(
                self._property_ctrl.open_dialog)
        elif self._model.type is PropType.POPUP_MENU:
            self._ui.property_value.clicked.connect(
                lambda: self._property_ctrl.open_popup_menu(
                    self._ui.property_value))

        """listen for model event signals"""
        self._model.value_changed.connect(
            self._ui.property_value.setText)

        """initialize view"""
        self._ui.property_name.setText(self._model.name)
        self._ui.property_value.set_unit(self._model.unit)
        self._ui.property_value.setText(self._model.value)

        if self._model.type is PropType.LINE_EDIT:
            self._ui.property_value.setReadOnly(False)
        else:
            self._ui.property_value.setReadOnly(True)
