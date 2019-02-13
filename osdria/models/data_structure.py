from PySide2.QtCore import *


class List(QObject):
    """representation of lists
    @param: list(Array)
    @function: add(QObject)
    @function: remove(Int)
    @signal: list_extended(QObject)
    @signal: list_reduced(Int)
    """
    list_extended = Signal(QObject)
    list_reduced = Signal(int)

    def __init__(self, list_input=[]):
        super(List, self).__init__()
        self._list = list_input

    def __getitem__(self, index):
        return self._list[index]

    def add(self, value):
        self._list.append(value)
        self.list_extended.emit(value)

    def remove(self, index):
        del self._list[index]
        self.list_reduced.emit(index)

    @property
    def list(self):
        return self._list


class Dict(QObject):
    """representation of dictionary
    @param: dict(Dict)
    @function: add(QObject)
    @function: remove(str)
    @signal: dict_extended(QObject)
    @signal: dict_reduced(str)
    """
    dict_extended = Signal(QObject)
    dict_reduced = Signal(str)

    def __init__(self, dict_input={}):
        super(Dict, self).__init__()
        self._dict = dict_input

    def items(self):
        return self._dict.items()

    def values(self):
        return self._dict.values()

    def add(self, name, value):
        self._dict[name] = value
        self.dict_extended.emit(name)

    def remove(self, name):
        del self._dict[name]
        self.dict_reduced.emit(name)

    @property
    def dict(self):
        return self._dict
