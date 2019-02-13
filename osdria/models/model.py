from PySide2.QtCore import QObject, Signal

from models.constants import OverviewSelection, PageType, SelectConnect, ZoomType
from models.scenario import Scenario
from models.element import *
from models.data_structure import *
from models.model_template import *


class Model(QObject):
    """application model
    @param: filename
    @param: newProject
    @function: save()
    @function: load()
    @signal: filename_changed(str)
    @signal: current_page_changed(OverviewType)
    @signal: overview_selection_changed(str)
    @signal: overview_properties_changed(List)
    @signal: scenarios_changed()
    @signal: current_scenario_changed()
    @signal: current_section_changed()
    @signal: energy_elements_changed()
    @signal: water_elements_changed()
    @signal: food_elements_changed()
    @signal: business_elements_changed()
    @signal: overview_sidebar_out_changed(Boolean)
    @signal: sections_sidebar_out_changed(Boolean)
    @signal: draft_sidebar_out_changed(Boolean)
    @signal: current_commodity_changed(Commodity)
    @signal: current_process_changed(Process)
    @signal: draft_select_mode_changed(SelectConnect)
    @signal: graph_zoom_mode_changed(ZoomType)
    """
    filename_changed = Signal(str)
    overview_selection_changed = Signal(int)
    overview_properties_changed = Signal(List)
    scenarios_changed = Signal()
    current_scenario_changed = Signal(QObject)
    current_section_changed = Signal(str)
    current_page_changed = Signal(int)
    energy_elements_changed = Signal()
    water_elements_changed = Signal()
    food_elements_changed = Signal()
    business_elements_changed = Signal()
    overview_sidebar_out_changed = Signal(bool)
    sections_sidebar_out_changed = Signal(bool)
    draft_sidebar_out_changed = Signal(bool)
    current_commodity_changed = Signal(QObject)
    current_process_changed = Signal(QObject)
    draft_select_mode_changed = Signal(int)
    graph_zoom_mode_changed = Signal(int)

    def __init__(self, filename, new_project=False):
        """initialise new or load existing model"""
        super(Model, self).__init__()
        self._filename = filename

        self._current_page = PageType.OVERVIEW
        self._current_section = PageType.OVERVIEW.name.title()
        self._overview_selection = OverviewSelection.OVERVIEW
        self._overview_properties = ModelTemplate.overview_properties()
        self._scenarios = ModelTemplate.scenarios()
        self._overview_sidebar_out = False
        self._sections_sidebar_out = False
        self._draft_sidebar_out = False

        if new_project is True:
            self.save()
        else:
            self.load()

    def save(self):
        """save model to file"""

    def load(self):
        """load model to file"""

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self.filename_changed.emit(value)

    @property
    def current_page(self):
        return self._current_page

    @current_page.setter
    def current_page(self, value):
        if value in PageType:
            self._current_page = value
            self.current_page_changed.emit(value.value)
        else:
            raise AttributeError

    @property
    def overview_selection(self):
        return self._overview_selection

    @overview_selection.setter
    def overview_selection(self, value):
        self._overview_selection = value
        self.overview_selection_changed.emit(value.value)

    @property
    def overview_properties(self):
        return self._overview_properties

    @overview_properties.setter
    def overview_properties(self, value):
        self._overview_properties = value
        self.overview_properties_changed.emit(value)

    @property
    def scenarios(self):
        return self._scenarios

    @scenarios.setter
    def scenarios(self, value):
        self._scenarios = value
        self.scenarios_changed.emit()

    @property
    def current_scenario(self):
        return self._current_scenario

    @current_scenario.setter
    def current_scenario(self, value):
        self._current_scenario = value
        self.current_scenario_changed.emit(value)

    @property
    def current_section(self):
        return self._current_section

    @current_section.setter
    def current_section(self, value):
        self._current_section = value
        self.current_section_changed.emit(value)

    @property
    def energy_elements(self):
        return self._energy_elements

    @energy_elements.setter
    def energy_elements(self, value):
        self._energy_elements = value
        self.energy_elements_changed.emit()

    @property
    def water_elements(self):
        return self._water_elements

    @water_elements.setter
    def water_elements(self, value):
        self._water_elements = value
        self.water_elements_changed.emit()

    @property
    def food_elements(self):
        return self._food_elements

    @food_elements.setter
    def food_elements(self, value):
        self._food_elements = value
        self.food_elements_changed.emit()

    @property
    def business_elements(self):
        return self._business_elements

    @business_elements.setter
    def business_elements(self, value):
        self._business_elements = value
        self.business_elements_changed.emit()

    @property
    def overview_sidebar_out(self):
        return self._overview_sidebar_out

    @overview_sidebar_out.setter
    def overview_sidebar_out(self, value):
        self._overview_sidebar_out = value
        self.overview_sidebar_out_changed.emit(value)

    @property
    def sections_sidebar_out(self):
        return self._sections_sidebar_out

    @sections_sidebar_out.setter
    def sections_sidebar_out(self, value):
        self._sections_sidebar_out = value
        self.sections_sidebar_out_changed.emit(value)

    @property
    def draft_sidebar_out(self):
        return self._draft_sidebar_out

    @draft_sidebar_out.setter
    def draft_sidebar_out(self, value):
        self._draft_sidebar_out = value
        self.draft_sidebar_out_changed.emit(value)

    @property
    def current_commodity(self):
        return self._current_commodity

    @current_commodity.setter
    def current_commodity(self, value):
        self._current_commodity = value
        self.current_commodity_changed.emit(value)

    @property
    def current_process(self):
        return self._current_process

    @current_process.setter
    def current_process(self, value):
        self._current_process = value
        self.current_process_changed(value)

    @property
    def draft_select_mode(self):
        return self._draft_select_mode

    @draft_select_mode.setter
    def draft_select_mode(self, value):
        if value in SelectConnect:
            self._draft_select_mode = value
            self.draft_select_mode_changed.emit(value.value)
        else:
            raise AttributeError

    @property
    def graph_zoom_mode(self):
        return self._graph_zoom_mode

    @graph_zoom_mode.setter
    def graph_zoom_mode(self, value):
        if value in ZoomType:
            self._graph_zoom_mode = value
            self.graph_zoom_mode_changed.emit(value.value)
        else:
            raise AttributeError

    @property
    def current_graph_commodity(self):
        return self._current_graph_commodity

    @current_graph_commodity.setter
    def current_graph_commodity(self, value):
        self._current_graph_commodity = value
        self.current_graph_commodity_changed.emit(value.value)
