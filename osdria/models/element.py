from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QVector2D, QVector4D, QIcon

from models.constants import ProcessCategory, OverviewSelection
from models.property import *
from models.data_structure import *

COMMODITY_NAME = "Commodity Name"


class ProcessCore(QObject):
    """data representing the process core
    @signal: name_changed()
    @signal: icon_changed()
    @signal: category_changed()
    @signal: section_changed()
    @signal: objective_function_changed()
    @signal: constraints_changed()"""
    name_changed = Signal()
    icon_changed = Signal()
    category_changed = Signal()
    section_changed = Signal()
    objective_function_changed = Signal()
    constraints_changed = Signal()

    def __init__(self):
        super(ProcessCore, self).__init__()
        self._name = ""
        self._icon = QIcon()
        self._category = ProcessCategory.SUPPLY
        self._section = OverviewSelection.ENERGY
        self.variables = Dict()
        self.data = Dict()
        self.properties = Dict()
        self.inputs = Dict()
        self.outputs = Dict()
        self._objective_function = ""
        self._constraints = ""

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        output << self._icon
        output.writeUInt32(self._category.value)
        output.writeUInt32(self._section.value)
        self.variables.write(output)
        self.data.write(output)
        self.properties.write(output)
        self.inputs.write(output)
        self.outputs.write(output)
        output.writeString(self._objective_function)
        output.writeString(self._constraints)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        input_ >> self._icon
        self._category = ProcessCategory(input_.readUInt32())
        self._section = OverviewSelection(input_.readUInt32())
        print(self._category.value)
        print(self._section.value)
        self.variables.read(input_)
        self.data.read(input_)
        self.properties.read(input_)
        self.inputs.read(input_)
        self.outputs.read(input_)
        self._objective_function = input_.readString()
        self._constraints = input_.readString()

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit()

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

    @constraints.setter
    def constraints(self, value):
        self._constraints = value
        self.constraints_changed.emit()


class Process(QObject):
    """data representing process object
    @param: name(str)
    @param: coordinate(QVector2D)
    @param: process_core(ProcessCore)
    @signal: name_changed()
    @signal: coordinate_changed()
    @signal: core_changed()"""
    name_changed = Signal()
    coordinate_changed = Signal()

    def __init__(self, name="", coordinate=QVector2D(), process_core=ProcessCore()):
        super(Process, self).__init__()
        self._name = name
        self._coordinate = coordinate
        self.core = process_core
        self.inputs = Dict()
        self.outputs = Dict()

        property_name = self.core.category.name.title() + " Name"
        name_property = Property(property_name, name, PropType.LINE_EDIT)
        self.properties = Dict({'name': name_property})
        self.define_core_properties()

    def write(self, output):
        """write data to output stream"""
        output << self._coordinate
        output.writeString(self.core.name)
        self.inputs.write(output)
        self.outputs.write(output)
        self.properties.write(output)

    def read(self, input_):
        """read data from input stream"""
        input_ >> self._coordinate
        self.core = self.define_core(input_.readString())
        self.inputs.read(input_)
        self.outputs.read(input_)
        self.properties.read(input_)

    def __str__(self):
        return self._name

    def define_core(self, name):
        """return core by name out of list of cores
        Question: access to list of cores?"""
        return ""

    def define_core_properties(self):
        """initialise properties of ProcessCore as templates"""
        for name, prop in self.core.properties.items():
            self.properties[name] = prop.copy()

    def convert(self):
        """convert objective function and constraints into executable
        optimization code with property values and input/outputs connections
        Additionally, error checking for missing inputs & outputs"""
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit()

    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, value):
        self._coordinate = value
        self.coordinate_changed.emit()


class CommodityType(QObject):
    """data representing commodity object
    @param: name
    @param: sub_commodities=[]
    @function: add_sub_commodity(SubCommodity)
    @function: remove_sub_commodity(int)
    @signal: sub_commodities_changed()"""

    def __init__(self, name=""):
        super(CommodityType, self).__init__()
        self._name = name
        self._coordinates = QVector4D(0, 0, 0, 0)
        self._properties = List()
        self._properties.add(
            Property(COMMODITY_NAME, name, PropType.LINE_EDIT))

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        output << self._coordinates
        self._properties.write(output)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        input_ >> self._coordinates
        self._properties.read(input_)

    def __str__(self):
        return self._name


class Commodity(QObject):
    """data representing a sub commodity
    @param: name
    @param: com_type(CommodityType)
    @signal: name_changed()
    @signal: type_changed()"""
    name_changed = Signal()
    type_changed = Signal()

    def __init__(self, name="", com_type=CommodityType()):
        super(Commodity, self).__init__()
        self._name = name
        self._type = com_type

    def write(self, output):
        """write data to output stream"""
        output.writeString(self._name)
        self._type.write(output)

    def read(self, input_):
        """read data from input stream"""
        self._name = input_.readString()
        self._type.read(input_)

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit()

    @property
    def com_type(self):
        return self._name

    @com_type.setter
    def com_type(self, value):
        self._type = value
        self.type_changed.emit()
