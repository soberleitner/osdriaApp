from PySide2.QtCore import QObject
from PySide2.QtWidgets import QFileDialog

from controllers.property_popup_ctrl import PropertyPopupCtrl
from controllers.property_dialog_ctrl import PropertyDialogCtrl
from views.property_popup_view import PropertyPopupView
from views.property_dialog_view import PropertyDialogView
from models.constants import ProcessCategory, OverviewSelection
from models.property import PropertyDialog, PropertyValue
from models.element import ProcessCore


class ProcessDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, model):
        super(ProcessDialogCtrl, self).__init__()
        self._model = model

    def open_process_popup(self, parent):
        popup_ctrl = PropertyPopupCtrl(self._model)
        popup_view = PropertyPopupView(parent, self._model, popup_ctrl)
        popup_view.show_popup()

    def open_section_popup(self, parent, section_model):
        section_model.value = OverviewSelection[parent.text().upper()]
        popup_ctrl = PropertyPopupCtrl(section_model)
        popup_view = PropertyPopupView(parent, section_model, popup_ctrl)
        popup_view.show_popup()

    def open_category_popup(self, parent, category_model):
        category_model.value = ProcessCategory[parent.text().upper()]
        popup_ctrl = PropertyPopupCtrl(category_model)
        popup_view = PropertyPopupView(parent, category_model, popup_ctrl)
        popup_view.show_popup()

    def change_variables(self, command, index, model):
        if command == "Edit":
            # Ignore edit command in variables (alternative workflow: delete & add)
            return

        dialog_model = PropertyDialog("Add Variable", [PropertyValue("Name")])
        dialog_ctrl = PropertyDialogCtrl(dialog_model)
        dialog_view = PropertyDialogView(dialog_model, dialog_ctrl)
        if not dialog_view.exec_():
            return

        key = dialog_model.values[0].value
        model.setData(key, "")

    def change_data(self, command, index, model):
        if command == "add":
            print("add data")
        else:
            print("edit data")

    def change_properties(self, command, index, model):
        if command == "add":
            print("add properties")
        else:
            print("edit properties")

    def change_commodities(self, command, index, model):
        if command == "add":
            print("add commodity")
        else:
            print("edit commodity")

    def transfer_data(self, new_process, name, section, category, icon, objective, constraints):
        if new_process:
            # create new process, add to current list and set it as current
            new_process = ProcessCore()
            self._model.choices.add(new_process)
            self._model.value = new_process

        self._model.value.name = name
        self._model.value.section = OverviewSelection[section.upper()]
        self._model.value.category = ProcessCategory[category.upper()]
        self._model.value.icon = icon
        self._model.value.objective_function = objective
        self._model.value.constraints = constraints
