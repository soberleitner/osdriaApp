from PySide2.QtCore import *


class Exports(QObject):
    """stores a specific list of export properties
    @param: folder_name
    @param: export_list
    @function: add(Export)
    @function: remove(Int)
    @signal: property_list_changed()
    @signal: folder_name_changed(str)"""
    export_list_changed = Signal()
    folder_name_changed = Signal(str)

    def __init__(self, folder_name, export_list=[]):
        super(Exports, self).__init__()
        self._export_list = export_list
        self.folder_name = folder_name

    def add(self, export):
        self._export_list.append(export)
        self.export_list_changed.emit()

    def remove(self, index):
        del self._export_list[index]
        self.export_list_changed.emit()

    @property
    def export_list(self):
        return self._export_list

    @property
    def folder_name(self):
        return self._folder_name

    @folder_name.setter
    def folder_name(self, value):
        self._folder_name = value
        self.folder_name_changed.emit(value)


class Export(QObject):
    """data stored for one export property
    @param: element
    @param: graph
    @param: dataset
    @param: period
    @signal: element_changed(Element)
    @signal: graph_changed(str)
    @signal: dataset_changed(str)
    @signal: period_changed(str)"""
    element_changed = Signal(Element)
    graph_changed = Signal(str)
    dataset_changed = Signal(str)
    period_changed = Signal(str)

    def __init__(self, element, graph, dataset, period):
        super(Property, self).__init__()
        self.element = element
        self.type = type

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value
        self.element_changed.emit(value)

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value):
        self._graph = value
        self.graph_changed.emit(value)

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        self._dataset = value
        self.dataset_changed.emit(value)

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, value):
        self._period = value
        self.period_changed.emit(value)
