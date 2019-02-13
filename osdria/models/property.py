from PySide2.QtCore import *

from models.data_structure import Dict
from models.constants import PropType


class PropertyLineEdit(QObject):
    """data stored for property of line edit
    @param: name
    @param: value
    @param: unit
    @signal: name_changed(str)
    @signal: value_changed(str)"""
    name_changed = Signal(str)
    value_changed = Signal(str)
    type = PropType.LINE_EDIT

    def __init__(self, name, value, unit=""):
        super(PropertyLineEdit, self).__init__()
        self._name = name
        self._value = PropertyValue(value, unit)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value.value = value
        self.value_changed.emit(value)


class PropertyDialog(PropertyLineEdit):
    """data stored for property with dialog input
    @param: name(str)
    @param: values({name: {value, unit}})
    @signal: value_changed(Dict)"""
    values_changed = Signal(Dict)
    type = PropType.DIALOG

    def __init__(self, name, values):
        super().__init__(name, "")
        self._values = Dict(values)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value
        self.values_changed(value)


class PropertyPopupMenu(PropertyLineEdit):
    """data stored for property with popup input
    @param: name
    @param: choices(List)"""
    type = PropType.POPUP_MENU

    def __init__(self, name, choices):
        super().__init__(name, choices[0])
        self._name = name
        self._choices = choices


class PropertyValue(QObject):
    """data stored for property value with unit information
    @param: value(str)
    @param: unit(str)
    @signal: value_changed(str)"""
    value_changed = Signal(str)

    def __init__(self, value, unit):
        super().__init__()
        self._value = value
        self._unit = unit

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.value_changed.emit(value)

    @property
    def unit(self):
        return self._unit
