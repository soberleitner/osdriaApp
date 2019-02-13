from PySide2.QtCore import QObject
from views.property_dialog_view import PropertyDialogView
from controllers.property_dialog_ctrl import PropertyDialogCtrl


class PropertyCtrl(QObject):
    """controller for property view"""
    def __init__(self, model):
        super(PropertyCtrl, self).__init__()
        self._model = model

    def change_property_value(self, value):
        self._model.value.value = str(value)

    def open_dialog(self):
        dialog_ctrl = PropertyDialogCtrl(self._model)
        dialog_view = PropertyDialogView(self._model, dialog_ctrl)
        dialog_view.exec_()

    def open_popup_menu(self):
        print("open popup: " + self._model.value.value)
