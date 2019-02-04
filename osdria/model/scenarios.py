from PySide2.QtCore import *
from properties import Property
from element import Element


class Scenarios(QObject):
    """stores a specific list of properties
    @param: scenario_list
    @function: add(Scenario)
    @function: remove(Int)
    @signal: scenario_list_changed()"""
    scenario_list_changed = Signal()

    def __init__(self, scenario_list=[]):
        super(Scenarios, self).__init__()
        self._scenario_list = scenario_list

    def add(self, scenario):
        self._scenario_list.append(scenario)
        self.scenario_list_changed.emit()

    def remove(self, index):
        del self._scenario_list[index]
        self.scenario_list_changed.emit()

    @property
    def scenario_list(self):
        return self._scenario_list


class Scenario(QObject):
    """stores data for scenario
    @param: name
    @param: property_list
    @function: add_property(ScenarioProperty)
    @function: remove_property(int)
    @signal: scenario_property_list_changed()"""
    scenario_property_list_changed = Signal()

    def __init__(self, name, property_list=[]):
        super(Scenario, self).__init__()
        self.name = name
        self._property_list = property_list

    def add_property(self, property):
        self._property_list.append(property)
        self.scenario_property_list_changed.emit()

    def remove_property(self, index):
        del self._property_list[index]
        self.scenario_property_list_changed.emit()

    @property
    def property_list(self):
        return self._property_list


class ScenarioProperty(QObject):
    """stores data for a property change in scenario
    @param: element
    @param: operator
    @param: prop
    @signal: element_changed(Element)
    @signal: operator_changed(str)
    @signal: property_changed(Property)"""
    element_changed = Signal(Element)
    operator_changed = Signal(str)
    property_changed = Signal(Property)

    def __init__(self, element, operator, prop):
        super(ScenarioProperty, self).__init__()
        self.element = element
        self.operator = operator
        self.prop = prop

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value
        self.element_changed.emit(value)

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = value
        self.operator_changed.emit(value)

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, value):
        self._prop = value
        self.property_changed.emit(value)
