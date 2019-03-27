from PySide2.QtCore import QObject

from models.constants import OverviewSelection, PageType, SelectConnect
from models.property import PropertyPopupMenu

from controllers.process_dialog_ctrl import ProcessDialogCtrl
from controllers.list_dialog_ctrl import ListDialogCtrl

from views.process_dialog_view import ProcessDialogView
from views.list_dialog_view import ListDialogView


class ProjectCtrl(QObject):
    """controller for project view"""
    def __init__(self, model):
        super(ProjectCtrl, self).__init__()
        self._model = model
        self.connect_model_data(self._model)

    def connect_model_data(self, model):
        """connect model data with references to other model data when model is loaded from file"""
        # connect process core in Process instance to ProcessCore instance
        for process in model.project_elements.process_list:
            process.core = list(filter(lambda core: core.name == process.core, model.process_cores))[0]

        # todo add necessary model connectors

    def save_model(self):
        self._model.save()

    # def open_time_series_dialog(self):
    #     time_series_ctrl = TimeSeriesDialogCtrl(self._model.time_series)
    #     time_series_view = TimeSeriesDialogView(self._model.time_series, time_series_ctrl)
    #     time_series_view.exec_()

    def open_commodity_dialog(self):
        commodities_ctrl = ListDialogCtrl(self._model.commodities)
        commodities_view = ListDialogView(self._model.commodities, commodities_ctrl)
        commodities_view.exec_()

    def open_process_dialog(self):
        dialog_model = PropertyPopupMenu("Process Cores", self._model.process_cores)
        process_ctrl = ProcessDialogCtrl(dialog_model, self._model.commodities)
        process_view = ProcessDialogView(dialog_model, process_ctrl)
        process_view.exec_()

    def open_scenario_dialog(self):
        print("open_scenario_dialog")

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
        self._model.current_section = self._model.overview_selection
        if page == PageType.OVERVIEW:
            self._model.overview_selection = OverviewSelection.OVERVIEW

        self._model.current_page = page

        if page == PageType.DRAFT:
            self._model.draft_select_mode = SelectConnect.SELECT

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
