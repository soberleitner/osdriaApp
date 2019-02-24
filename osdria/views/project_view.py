from PySide2.QtWidgets import *
from PySide2.QtCore import Qt

from views.project_view_ui import Ui_MainWindow
from models.constants import OverviewSelection, PageType, SelectConnect, ZoomType


class ProjectView(QMainWindow):
    """Main Project window"""

    def __init__(self, model, project_controller):
        super(ProjectView, self).__init__()

        self._model = model
        self._project_ctrl = project_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        # menu bar
        self._ui.action_save.triggered.connect(self._project_ctrl.save_model)
        self._ui.action_close.triggered.connect(self.close)
        self._ui.action_commodities.triggered.connect(
            self._project_ctrl.open_commodity_dialog)
        self._ui.action_processes.triggered.connect(
            self._project_ctrl.open_process_dialog)
        self._ui.action_scenarios.triggered.connect(
            self._project_ctrl.open_scenario_dialog)
        self._ui.action_execute.triggered.connect(
            self._project_ctrl.run_optimization)
        # overview toolbar
        self._ui.tool_scenarios.clicked.connect(
            self._project_ctrl.open_scenario_dialog)
        self._ui.scenario_select.clicked.connect(
            lambda: self._project_ctrl.show_scenario_selection(
                self._ui.scenario_select))
        self._ui.tool_run.clicked.connect(self._project_ctrl.run_optimization)
        self._ui.tool_export.clicked.connect(
            self._project_ctrl.open_export_dialog)
        self._ui.tool_sidebar_overview.clicked.connect(
            lambda: self._project_ctrl.toggle_sidebar(PageType.OVERVIEW))
        # overview content
        self._ui.logo.hovered.connect(self._project_ctrl.change_icon)
        self._ui.logo.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.SECTIONS))
        # sections toolbar
        self._ui.tool_back_sections.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.OVERVIEW))
        self._ui.tool_draft.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.DRAFT))
        self._ui.tool_graph.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.GRAPH))
        self._ui.tool_sidebar_sections.clicked.connect(
            lambda: self._project_ctrl.toggle_sidebar(PageType.SECTIONS))
        # sections content

        # draft toolbar
        self._ui.tool_back_draft.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.SECTIONS))
        self._ui.tool_cursor.clicked.connect(
            lambda: self._project_ctrl.toggle_select_connect(
                SelectConnect.SELECT))
        self._ui.tool_connect.clicked.connect(
            lambda: self._project_ctrl.toggle_select_connect(
                SelectConnect.CONNECT))
        self._ui.tool_sidebar_draft.clicked.connect(
            lambda: self._project_ctrl.toggle_sidebar(PageType.DRAFT))
        # draft content

        # graph toolbar
        self._ui.tool_back_graph.clicked.connect(
            lambda: self._project_ctrl.change_page(PageType.SECTIONS))
        self._ui.select_commodity.currentIndexChanged.connect(
            self._project_ctrl.change_graph_commodity)
        self._ui.tool_export_graph.clicked.connect(
            self._project_ctrl.open_export_dialog)
        self._ui.tool_cursor_graph.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.SELECT))
        self._ui.tool_zoom_in.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.ZOOM_IN))
        self._ui.tool_zoom_out.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.ZOOM_OUT))
        self._ui.tool_zoom_range.clicked.connect(
            lambda: self._project_ctrl.change_zoom_mode(ZoomType.ZOOM_RANGE))
        # graph content

        """listen for model event signals"""
        # stacked pages
        self._model.current_page_changed.connect(
            self._ui.stacked_pages.setCurrentIndex)
        # overview page
        self._model.scenarios.value_changed.connect(
            lambda: self._ui.scenario_select.setText(str(self._model.scenarios.value)))
        self._model.overview_selection_changed.connect(
            self.on_selection_change)
        self._model.overview_properties_changed.connect(
            self._ui.sidebar_overview.load_data)
        self._model.overview_sidebar_out_changed.connect(
            self._ui.sidebar_overview.toggle)

        # sections page
        self._model.current_section_changed.connect(
            self.on_section_change)
        self._model.sections_sidebar_out_changed.connect(
            self._ui.sidebar_sections.toggle)

        # draft page
        self._model.draft_select_mode_changed.connect(
            self.on_select_mode_change)
        self._model.draft_sidebar_out_changed.connect(
            self._ui.sidebar_draft.toggle)

        # graph page
        self._model.graph_zoom_mode_changed.connect(
            self.on_zoom_mode_change)
        self._model.current_commodity_changed.connect(
            self.on_commodity_change)

        """initialise view"""
        self._ui.stacked_pages.setCurrentIndex(OverviewSelection.OVERVIEW.value)
        self._ui.scenario_select.setReadOnly(True)
        self._ui.scenario_select.set_popup(True)
        self._ui.scenario_select.setText(str(self._model.scenarios.value))
        self._ui.sidebar_overview.load_data(self._model.overview_properties)

    def on_selection_change(self, selection):
        self._ui.logo.change_icon(OverviewSelection(selection))
        self._ui.title_overview.setText(str(OverviewSelection(selection)))

    def on_section_change(self, section):
        self._ui.title_sections.setText(section)
        self._ui.title_draft.setText(section + " - Draft")

    def on_select_mode_change(self, select_type):
        self._ui.tool_cursor.setChecked(False)
        self._ui.tool_connect.setChecked(False)

        if SelectConnect(select_type) is SelectConnect.SELECT:
            self._ui.tool_cursor.setChecked()
        else:
            self._ui.tool_connect.setChecked()

    def on_zoom_mode_change(self, zoom_value):
        self._ui.tool_cursor_graph.setChecked(False)
        self._ui.tool_zoom_in.setChecked(False)
        self._ui.tool_zoom_out.setChecked(False)
        self._ui.tool_zoom_range.setChecked(False)

        zoom_type = ZoomType(zoom_value)
        if zoom_type is ZoomType.SELECT:
            self._ui.tool_cursor_graph.setChecked()
        elif zoom_type is ZoomType.ZOOM_IN:
            self._ui.tool_zoom_in.setChecked()
        elif zoom_type is ZoomType.ZOOM_OUT:
            self._ui.tool_zoom_out.setChecked()
        else:
            self._ui.tool_zoom_range.setChecked()

    def on_commodity_change(self, commodity):
        if commodity is not None:
            self._ui.tool_graph.show()
            self._ui.title_graph.setText(commodity.name)
        else:
            self._ui.tool_graph.hide()

    def closeEvent(self, event):
        self._model.save()
