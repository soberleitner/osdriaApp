from PySide2.QtCore import *
from models.property import Property
from models.element import Process
from models.data_structure import List


class Scenario(List):
    """stores data for scenario
    @param: name
    @param: property_list
    @signal: name_changed(str)"""
    name_changed = Signal(str)

    def __init__(self, name, property_list):
        super(Scenario, self).__init__(property_list)
        self._name = name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)


class ScenarioProperty(QObject):
    """stores data for a property change in scenario
    @param: element
    @param: operator
    @param: prop
    @signal: element_changed(Element)
    @signal: operator_changed(str)
    @signal: property_changed(Property)"""
    element_changed = Signal(QObject)
    operator_changed = Signal(str)
    property_changed = Signal(QObject)

    def __init__(self, element, operator, prop):
        super(ScenarioProperty, self).__init__()
        self._element = element
        self._operator = operator
        self._prop = prop

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
