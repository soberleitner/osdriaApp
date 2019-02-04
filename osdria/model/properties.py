from PySide2.QtCore import *


class Properties(QObject):
    """stores a specific list of properties
    @param: property_list
    @function: add(Property)
    @function: remove(Int)
    @Signal: property_list_changed()"""
    property_list_changed = Signal()

    def __init__(self, property_list=[]):
        super(Properties, self).__init__()
        self._property_list = property_list

    def add(self, property):
        self._property_list.append(property)
        self.property_list_changed.emit()

    def remove(self, index):
        del self._property_list[index]
        self.property_list_changed.emit()

    @property
    def property_list(self):
        return self._property_list


class Property(QObject):
    """data stored for one property
    @param: name
    @param: value
    @param: type
    @signal: name_changed(str)
    @signal: value_changed(str, float)"""
    name_changed = Signal(str)
    value_changed = Signal((str), (float))

    def __init__(self, name, value, type):
        super(Property, self).__init__()
        self.name = name
        self.value = value
        self.type = type

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
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
