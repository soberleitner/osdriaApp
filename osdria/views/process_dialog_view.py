from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import *

from models.constants import OverviewSelection, ProcessCategory
from models.property import PropertyPopupMenu
from models.data_structure import List

from views.process_dialog_view_ui import Ui_ProcessDialog
from views.components.property_edit import PropertyEdit
from views.components.process_list_view import ListModel

ICON_FILE = "Image files (*.png)"


class ProcessDialogView(QDialog):
    """Process Dialog View"""

    def __init__(self, process_dialog_model, process_dialog_controller):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super(ProcessDialogView, self).__init__(None, settings)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._model = process_dialog_model
        self._section_popup_model = PropertyPopupMenu("Sections", List(list(OverviewSelection)[1:]))
        self._category_popup_model = PropertyPopupMenu("Categories", List(list(ProcessCategory)))
        self._ctrl = process_dialog_controller
        self._ui = Ui_ProcessDialog()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        self._ui.process_name.clicked.connect(self.on_process_click)
        self._ui.button_add.clicked.connect(self.on_add_click)
        self._ui.section_value.clicked.connect(
            lambda: self._ctrl.open_section_popup(self._ui.section_value, self._section_popup_model))
        self._ui.category_value.clicked.connect(
            lambda: self._ctrl.open_category_popup(self._ui.category_value, self._category_popup_model))
        self._ui.button_icon.clicked.connect(self.open_icon_dialog)
        self._ui.variables_list.edit_add.connect(self._ctrl.change_variables)
        self._ui.data_list.edit_add.connect(self._ctrl.change_data)
        self._ui.properties_list.edit_add.connect(self._ctrl.change_properties)
        self._ui.inputs_list.edit_add.connect(self._ctrl.change_commodities)
        self._ui.outputs_list.edit_add.connect(self._ctrl.change_commodities)
        self._ui.cancel_button.clicked.connect(self.reject)
        self._ui.apply_button.clicked.connect(self.accept)
        self.accepted.connect(self.gather_data)

        """listen for model event signals"""
        self._model.value_changed.connect(self.on_process_change)
        self._section_popup_model.value_changed.connect(
            lambda: self._ui.section_value.setText(str(self._section_popup_model.value)))
        self._category_popup_model.value_changed.connect(
            lambda: self._ui.category_value.setText(str(self._category_popup_model.value)))

        """initialize view"""
        self._new_process = False
        self._ui.process_name.setReadOnly(False)
        self._ui.process_name.set_popup(True)
        self._ui.section_value.setReadOnly(True)
        self._ui.section_value.set_popup(True)
        self._ui.category_value.setReadOnly(True)
        self._ui.category_value.set_popup(True)
        self._ui.objective_value.setAttribute(Qt.WA_MacShowFocusRect, 0)
        if not self._model.value:
            print("not model.value")
            self._new_process = True
            self.init_content()
        else:
            print("existing model.value")
            self.load_content(self._model.value)

    def init_content(self):
        """initialise new process with empty inputs"""
        self._ui.process_name.setText("New Process")
        self._ui.section_value.setText(OverviewSelection.ENERGY)
        self._ui.category_value.setText(ProcessCategory.SUPPLY)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/img/process_icon@2x.png"), QIcon.Normal, QIcon.Off)
        self._ui.button_icon.setIcon(icon)
        self._ui.variables_list.setModel(ListModel())
        # self._ui.data_list.setModel(ListModel())
        # self._ui.properties_list.setModel(ListModel())
        # self._ui.inputs_list.setModel(ListModel())
        # self._ui.outputs_list.setModel(ListModel())
        self._ui.objective_value.setText("Process Objective Function")
        self._ui.constraints_value.setText("Process Constraints")
        self._new_process = True
        print("init_content finished")

    def load_content(self, process):
        print("Process name:")
        print(process.name)
        self._ui.process_name.setText(str(process.name))
        self._ui.section_value.setText(str(process.section))
        self._ui.category_value.setText(str(process.category))
        self._ui.button_icon.setIcon(process.icon)
        # self._ui.variables_list.setModel(ListModel(process.variables))
        # self._ui.data_list.setModel(ListModel(process.data))
        # self._ui.properties_list.setModel(ListModel(process.properties))
        # self._ui.inputs_list.setModel(ListModel(process.inputs))
        # self._ui.outputs_list.setModel(ListModel(process.outputs))
        self._ui.objective_value.setText(str(process.objective_function))
        self._ui.constraints_value.setText(str(process.constraints))

    def on_process_click(self):
        """transfer all data of current process to general model"""
        self.gather_data()
        self._ctrl.open_process_popup(self._ui.process_name)

    def on_process_change(self):
        self._ui.process_name.setText(str(self._model.value))
        self.load_content(self._model.value)

    def on_add_click(self):
        """save process and initialise new one"""
        self.gather_data()
        self.init_content()

    def open_icon_dialog(self):
        filename = QFileDialog.getOpenFileName(self._ui.dialog_frame,
                                               "Choose process icon",
                                               "/home",
                                               ICON_FILE)
        icon_size = self._ui.button_icon.iconSize()
        icon = QIcon()
        icon.addPixmap(QPixmap(filename[0]), QIcon.Normal, QIcon.Off)
        self._ui.button_icon.setIcon(icon)
        self._ui.button_icon.setIconSize(icon_size)

    def gather_data(self):
        """transfer edited data to model"""
        self._ctrl.transfer_data(
            self._new_process,
            self._ui.process_name.text(),
            self._ui.section_value.text(),
            self._ui.category_value.text(),
            self._ui.button_icon.icon(),
            self._ui.objective_value.text(),
            self._ui.constraints_value.toPlainText()
        )
        self._new_process = False

    def keyPressEvent(self, event):
        """prevent dialog closing with enter or return key"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        super().keyPressEvent(event)


