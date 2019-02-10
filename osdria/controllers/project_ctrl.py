from PySide2.QtCore import QObject
from models.constants import OverviewSelection, PageType


class ProjectCtrl(QObject):
    """controller for project view"""
    def __init__(self, model):
        super(ProjectCtrl, self).__init__()
        self._model = model

    def open_scenario_dialog(self):
        print("open_scenario_dialog")

    def change_scenario(self, index):
        self._model.current_scenario = self._model.scenarios[index]
        print("change_scenario to: " + self._model.current_scenario.name)

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
