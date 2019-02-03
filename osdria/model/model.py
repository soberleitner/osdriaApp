from PySide2.QtCore import *


class Model(QObject):
    """application model"""
    filename_changed = Signal(str)

    def __init__(self, filename):
        super(Model, self).__init__()
        self.filename = filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self.filename_changed.emit(value)
