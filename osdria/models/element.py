from PySide2.QtCore import QObject, Signal

from models.constants import ProcessCategory
from models.property import *
from models.data_structure import *

COMMODITY_NAME = "Commodity Name"


class ProcessCore(QObject):
    """data representing the process core
    @signal: icon_changed(str)
    @signal: category_changed(ProcessCategory)
    @signal: objective_function_changed(str)"""
    icon_changed = Signal(str)
    category_changed = Signal(QObject)
    objective_function_changed = Signal(str)

    def __init__(self):
        super(ProcessCore, self).__init__()
        self._icon = ""
        self._category = 0
        self._objective_function = ""
        self._properties = List()
        self._constraints = List()
        self._inputs = Dict()
        self._outputs = Dict()

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.icon_changed.emit(value)

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value in ProcessCategory:
            self._category = value
            self.category_changed.emit(value)
        else:
            raise AttributeError

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, value):
        self._properties = value

    @property
    def objective_function(self):
        return self._objective_function

    @objective_function.setter
    def objective_function(self, value):
        self._objective_function = value
        self.objective_function_changed.emit(value)

    @property
    def constraints(self):
        return self._constraints

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs


class Process(QObject):
    """data representing process object
    @param: name(str)
    @param: coordinate([Int, Int])
    @param: process_core(ProcessCore)
    @signal: coordinate_changed([Int, Int])
    @signal: core_changed(ProcessCore)"""
    coordinate_changed = Signal([int, int])
    core_changed = Signal(QObject)

    def __init__(self, name, coordinate, process_core):
        super(Process, self).__init__()
        self._coordinate = coordinate
        self._core = process_core
        property_name = self._core.category.name.title() + " Name"
        name_property = Property(property_name, name, PropType.LINE_EDIT)
        self._core.properties.add(name_property)

    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, value):
        self._coordinate = value
        self.coordinate_changed.emit(value)

    @property
    def core(self):
        return self._core

    @core.setter
    def core(self, value):
        self._core = value
        self.core_changed.emit(value)


class Commodity(List):
    """data representing commodity object
    @param: name
    @param: icon
    @param: sub_commodities=[]
    @function: add_sub_commodity(SubCommodity)
    @function: remove_sub_commodity(int)
    @signal: sub_commodities_changed()"""

    def __init__(self, name, icon, sub_commodities):
        super(Commodity, self).__init__(sub_commodities)
        self._icon = icon
        self._coordinates = ([0, 0], [0, 0])
        self._sub_commodities = sub_commodities
        self._properties = List()
        self._properties.add(
            Property(COMMODITY_NAME, name, PropType.LINE_EDIT))


class SubCommodity(QObject):
    """data representing a sub commodity
    @param: name
    @signal: name_changed(str)"""
    name_changed = Signal(str)

    def __init__(self, name):
        super(SubCommodity, self).__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)
