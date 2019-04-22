from PySide2.QtCore import QObject, QCoreApplication

from core.optimization_tool import Optimizer


class OptimizationDialogCtrl(QObject):
    """controller for property dialog view"""
    def __init__(self, project_elements):
        super(OptimizationDialogCtrl, self).__init__()
        self._optimizer = None
        self._model = project_elements

    def run_optimization(self):
        self._optimizer = Optimizer(self._model.process_list, self._model.commodity_list)

        self._model.optimization_text = "Converting Optimization Code"
        QCoreApplication.processEvents()
        self._optimizer.translate()

        self._model.optimization_text = "Running Optimization"
        QCoreApplication.processEvents()
        self._optimizer.solve()

        self._model.optimization_text = "Retrieving Results"
        QCoreApplication.processEvents()
        self._optimizer.set_results()

        QCoreApplication.processEvents()
        self._model.optimization_text = "DONE"

    def get_model(self):
        return self._optimizer.get_model()

    def cancel_optimization(self):
        self._optimizer.cancel()
