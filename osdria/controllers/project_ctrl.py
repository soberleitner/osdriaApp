from PySide2.QtCore import QObject
from models.constants import OverviewSelection, PageType
from models.property import PropertyPopupMenu
from controllers.property_popup_ctrl import PropertyPopupCtrl
from controllers.process_dialog_ctrl import ProcessDialogCtrl
from views.property_popup_view import PropertyPopupView
from views.process_dialog_view import ProcessDialogView



class ProjectCtrl(QObject):
    """controller for project view"""
    def __init__(self, model):
        super(ProjectCtrl, self).__init__()
        self._model = model

    def save_model(self):
        self._model.save()

    def open_commodity_dialog(self):
        print("open_commodity_dialog")

    def open_process_dialog(self):
        dialog_model = PropertyPopupMenu("Process Cores", self._model.process_cores)
        process_ctrl = ProcessDialogCtrl(dialog_model)
        process_view = ProcessDialogView(dialog_model, process_ctrl)
        print("before process view exec")
        process_view.exec_()
        print("after process view exec")

    def open_scenario_dialog(self):
        print("open_scenario_dialog")

    def show_scenario_selection(self, parent):
        popup_ctrl = PropertyPopupCtrl(self._model.scenarios)
        popup_view = PropertyPopupView(parent, self._model.scenarios, popup_ctrl)
        popup_view.show_popup()

    def run_optimization(self):
        print("run_optimization")

    def open_export_dialog(self):
        print("open_export_dialog")

    def toggle_sidebar(self, page):
        if page is PageType.OVERVIEW:
            self._model.overview_sidebar_out = not self._model.overview_sidebar_out
        elif page is PageType.SECTIONS:
            self._model.sections_sidebar_out = not self._model.sections_sidebar_out
        elif page is PageType.DRAFT:
            self._model.draft_sidebar_out = not self._model.draft_sidebar_out

    def change_icon(self, selection_type):
        self._model.overview_selection = OverviewSelection(selection_type)

    def change_page(self, page):
        self._model.current_section = self._model.overview_selection.name.title()
        self._model.current_page = page

    def toggle_select_connect(self, select_type):
        self._model.draft_select_mode = select_type

    def change_graph_commodity(self, index):
        """first entry of commodity combo box is commodity,
        others are sub commodities"""
        if index > 1:
            com = self._model.current_commodity.sub_commodities[index - 1]
        else:
            com = self._model.current_graph_commodity

        self._model.current_graph_commodity = com

    def change_zoom_mode(self, zoom_type):
        self._model.graph_zoom_mode = zoom_type
