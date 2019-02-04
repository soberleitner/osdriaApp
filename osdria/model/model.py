from PySide2.QtCore import *
from scenarios import Scenario


class Model(QObject):
    """application model
    @param: filename
    @param: newProject
    @function: save()
    @function: load()
    @signal: filename_changed(str)
    @signal: current_stacked_page_changed(int)
    @signal: overview_selection_changed(str)
    @signal: scenarios_changed()
    @signal: current_scenario_changed()
    @signal: current_section_changed()
    @signal: energy_elements_changed()
    @signal: water_elements_changed()
    @signal: food_elements_changed()
    @signal: business_elements_changed()"""
    filename_changed = Signal(str)
    current_stacked_page_changed = Signal(int)
    overview_selection_changed = Signal(str)
    scenarios_changed = Signal()
    current_scenario_changed = Signal(Scenario)
    current_section_changed = Signal(str)
    energy_elements_changed = Signal()
    water_elements_changed = Signal()
    food_elements_changed = Signal()
    business_elements_changed = Signal()

    def __init__(self, filename, newProject=False):
        """initialises new model or load existing model"""
        super(Model, self).__init__()
        self.filename = filename

        if newProject is True:
            self.init()
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
    def current_stacked_page(self):
        return self._current_stacked_page

    @current_stacked_page.setter
    def current_stacked_page(self, value):
        self._current_stacked_page = value
        self.current_stacked_page_changed.emit(value)

    @property
    def overview_selection(self):
        return self._overview_selection

    @overview_selection.setter
    def overview_selection(self, value):
        self._overview_selection = value
        self.overview_selection_changed.emit(value)

    @property
    def overview_properties(self):
        return self._overview_properties

    @overview_properties.setter
    def overview_properties(self, value):
        self._overview_properties = value
        self.overview_properties_changed.emit()

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
