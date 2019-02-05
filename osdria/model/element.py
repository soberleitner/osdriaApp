from PySide2.QtCore import *

from properties import *

COMMODITY_NAME = "Commodity Name"


class Process(QObject):
    """data representing process object"""
    def __init__(self, name, icon, input={}, output={}):
        super(Process, self).__init__()
        self.name = name
        self.icon = icon
        self.input = input
        self.output = output
        self.objective_function = 0
        self.constraints = []


class Commodity(QObject):
    """data representing commodity object
    @param: name
    @param: icon
    @param: sub_commodities=[]
    @function: add_sub_commodity(SubCommodity)
    @function: remove_sub_commodity(int)
    @signal: sub_commodities_changed()"""
    sub_commodities_changed = Signal()

    def __init__(self, name, icon, sub_commodities=[]):
        super(Commodity, self).__init__()
        self.icon = icon
        self.coordinates = ([0, 0], [0, 0])
        self.sub_commodities = sub_commodities
        self.properties = Properties()
        self.properties.add(
            Property(COMMODITY_NAME, name, PropType.LINE_EDIT))

    def add_sub_commodity(self, sub_commodity):
        self.sub_commodities.append(sub_commodity)
        self.sub_commodities_changed.emit()

    def remove_sub_commodity(self, index):
        del self.sub_commodities[index]
        self.sub_commodities_changed.emit()


class SubCommodity(QObject):
    """data representing a subcommodity
    @param: name
    @signal: name_changed(str)"""
    name_changed = Signal(str)

    def __init__(self, name):
        super(SubCommodity, self).__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.name_changed.emit(name)
