from PySide2.QtCore import *
from properties import Property


class Elements(QObject):
    """stores a specific list of elements
    @param: element_list
    @function: add(Element)
    @function: remove(Int)
    @signal: element_list_changed()"""
    element_list_changed = Signal()

    def __init__(self, scenario_list=[]):
        super(Scenarios, self).__init__()
        self._scenario_list = scenario_list

    def add_commodity(self, commodity):
        self._element_list.append(element)
        self.elemen_list_changed.emit()

    def remove_commodity(self, index):
        del self._element_list[index]
        self.element_list_changed.emit()

    def add_process(self, process):

    def remove_process(self, index):


    def add_demand(self, demand):

    def remove_demand(self, index):

    @property
    def scenario_list(self):
        return self._element_list