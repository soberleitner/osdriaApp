from PySide2.QtCore import QObject

from models.constants import PropType


class PropertyDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, model):
        super(PropertyDialogCtrl, self).__init__()
        self._model = model
        self.create_display_value()

    def set_property_values(self, value_list):
        for model_value, dialog_value in zip(self._model.values.values(), value_list):
            model_value.value = dialog_value
        if self._model.type is PropType.DIALOG:
            self.create_display_value()

    def create_display_value(self):
        display_value = ""
        for value in self._model.values.values():
            if display_value is "":
                display_value = value.value
            else:
                display_value += ", " + value.value
            if value.unit is not "":
                display_value += " " + value.unit
        self._model.value = display_value
