from PySide2.QtCore import QObject


class ProjectCtrl(QObject):
    """controller for project view"""
    def __init__(self, model):
        super(ProjectCtrl, self).__init__()
        self._model = model
