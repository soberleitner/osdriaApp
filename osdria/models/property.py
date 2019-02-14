from PySide2.QtCore import *

from models.data_structure import List
from models.constants import PropType


class PropertyValue(QObject):
    """data stored for property value with unit information
    @param: name(str)
    @param: value(str)
    @param: unit(str)
    @signal: value_changed(str)"""
    name_changed = Signal(str)
    value_changed = Signal(str)

    def __init__(self, name, value, unit):
        super().__init__()
        self._name = name
        self._value = value
        self._unit = unit

    def __str__(self):
        """create display value if string is requested"""
        display_value = self._value
        if self._unit != "":
            display_value += " " + self._unit
        return display_value

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
        self._value = value
        self.value_changed.emit(value)

    @property
    def unit(self):
        return self._unit


class PropertyValueTimeSeries(PropertyValue):
    """data stored for property value representing a times series
    @param: name
    @param: value(List)
    @param: unit
    @signal: name_changed(str)
    @signal: value_changed()"""
    name_changed = Signal(str)
    value_changed = Signal()

    def __init__(self, name, value, unit):
        super().__init__(name, "", unit)
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class PropertyLineEdit(PropertyValue):
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
        super().__init__(name, value, unit)


class PropertyDialog(PropertyLineEdit):
    """data stored for property with dialog input
    @param: name(str)
    @param: values({name: PropertyValue})
    @signal: name_changed(str)
    @signal: value_changed(Dict)"""
    name_changed = Signal(str)
    values_changed = Signal(List)
    type = PropType.DIALOG

    def __init__(self, name, values):
        super().__init__(name, "")
        self._values = List(values)
        # create display value for sub-property properties
        display_text = ", ".join(map(str, values))
        PropertyDialog.value.fset(self, display_text)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value
        self.values_changed.emit(value)


class PropertyPopupMenu(PropertyLineEdit):
    """data stored for property with popup input
    @param: name
    @param: choices(List)
    @signal: name_changed(str)
    @signal: value_changed(str)
    @signal: choices_changed()"""
    name_changed = Signal(str)
    value_changed = Signal(str)
    choices_changed = Signal()
    type = PropType.POPUP_MENU

    def __init__(self, name, choices=[]):
        super().__init__(name, choices[0].name)
        self._choices = choices

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        self._choices = value
        self.choices_changed.emit()
