from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QVector2D, QVector4D, QIcon

from models.constants import ProcessCategory, OverviewSelection
from models.property import *
from models.data_structure import *

COMMODITY_NAME = "Commodity Name"


class ProcessCore(QObject):
    """data representing the process core
    @signal: icon_changed(QIcon)
    @signal: category_changed(ProcessCategory)
    @signal: objective_function_changed(str)"""
    icon_changed = Signal()
    category_changed = Signal()
    section_changed = Signal()
    objective_function_changed = Signal()

    def __init__(self):
        super(ProcessCore, self).__init__()
        self._icon = QIcon()
        self._category = ProcessCategory.SUPPLY
        self._section = OverviewSelection.ENERGY
        self._properties = List()
        self._objective_function = ""
        self._constraints = List()
        self._inputs = Dict()
        self._outputs = Dict()

    def write(self, output):
        """write data to output stream"""
        output << self._icon
        output.writeUInt32(self._category.value)
        output.writeUInt32(self._section.value)
        self._properties.write(output)
        output.writeString(self._objective_function)
        self._constraints.write(output)
        self._inputs.write(output)
        self._outputs.write(output)

    def read(self, input_):
        """read data from input stream"""
        input_ >> self._icon
        self._category.value = input_.readUInt32()
        self._section.value = input_.readUInt32()
        self._properties.read(input_)
        self._objective_function = input_.readString()
        self._constraints.read(input_)
        self._inputs.read(input_)
        self._outputs.read(input_)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.icon_changed.emit()

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, value):
        if value in OverviewSelection:
            self._section = value
            self.section_changed.emit()
        else:
            raise AttributeError

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value in ProcessCategory:
            self._category = value
            self.category_changed.emit()
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
        self.objective_function_changed.emit()

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
    @param: section(OverviewSelection)
    @param: coordinate([Int, Int])
    @param: process_core(ProcessCore)
    @signal: coordinate_changed([Int, Int])
    @signal: core_changed(ProcessCore)"""
    coordinate_changed = Signal()
    core_changed = Signal()

    def __init__(self, name="", coordinate=QVector2D(), process_core=ProcessCore()):
        super(Process, self).__init__()
        self._coordinate = coordinate
        self._core = process_core
        property_name = self._core.category.name.title() + " Name"
        name_property = Property(property_name, name, PropType.LINE_EDIT)
        self._core.properties.add(name_property)

    def write(self, output):
        """write data to output stream"""
        output << self._coordinate
        self._core.write(output)

    def read(self, input_):
        """read data from input stream"""
        input_ >> self._coordinate
        self._core.read(input_)

    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, value):
        self._coordinate = value
        self.coordinate_changed.emit()

    @property
    def core(self):
        return self._core

    @core.setter
    def core(self, value):
        self._core = value
        self.core_changed.emit()


class Commodity(List):
    """data representing commodity object
    @param: name
    @param: icon
    @param: sub_commodities=[]
    @function: add_sub_commodity(SubCommodity)
    @function: remove_sub_commodity(int)
    @signal: sub_commodities_changed()"""

    def __init__(self, name="", icon=QIcon(), sub_commodities=[]):
        super(Commodity, self).__init__(sub_commodities)
        self._icon = icon
        self._coordinates = QVector4D(0, 0, 0, 0)
        self._sub_commodities = List(sub_commodities)
        self._properties = List()
        self._properties.add(
            Property(COMMODITY_NAME, name, PropType.LINE_EDIT))

    def write(self, output):
        """write data to output stream"""
        output << self._icon
        output << self._coordinates
        self._sub_commodities.write(output)
        self._properties.write(output)

    def read(self, input_):
        """read data from input stream"""
        input_ >> self._icon
        input_ >> self._coordinates
        self._sub_commodities.read(input_)
        self._properties.read(input_)


class SubCommodity(QObject):
    """data representing a sub commodity
    @param: name
    @signal: name_changed(str)"""
    name_changed = Signal(str)

    def __init__(self, name=""):
        super(SubCommodity, self).__init__()
        self._name = name

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)
