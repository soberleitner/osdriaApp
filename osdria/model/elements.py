from PySide2.QtCore import *


class Elements(QObject):
    """stores a specific list of elements
    @param: commodity_list
    @param: process_list
    @function: add_commodity(Commodity)
    @function: remove_commodity(Int)
    @function: add_process(Process)
    @function: remove_process(Int)
    @signal: commodity_list_changed()
    @signal: process_list_changed()"""
    commodity_list_changed = Signal()
    process_list_changed = Signal()

    def __init__(self, commodity_list=[], process_list=[]):
        super(Elements, self).__init__()
        self._commodity_list = commodity_list
        self._process_list = process_list

    def add_commodity(self, commodity):
        self._commodity_list.append(commodity)
        self.commodity_list_changed.emit()

    def remove_commodity(self, index):
        del self._commodity_list[index]
        self.commodity_list_changed.emit()

    def add_process(self, process):
        self._process_list.append(process)
        self.process_list_changed.emit()

    def remove_process(self, index):
        del self._process_list[index]
        self.process_list_changed.emit()

    @property
    def commodity_list(self):
        return self._commodity_list

    @property
    def process_list(self):
        return self._process_list
