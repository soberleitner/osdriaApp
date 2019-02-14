from PySide2.QtCore import QObject

from models.constants import PropType


class PropertyPopupCtrl(QObject):
    """controller for property popup view"""
    def __init__(self, popup_model):
        super(PropertyPopupCtrl, self).__init__()
        self._model = popup_model

    def set_popup_value(self, action):
        """move selected item to beginning of list and set """
        index = action.data()
        self._model.choices.insert(0, self._model.choices.pop(index))
        self._model.value = self._model.choices[0].name
