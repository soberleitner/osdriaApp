from PySide2.QtCore import QObject

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
        self._optimizer.translate()

        self._model.optimization_text = "Running Optimization"
        self._optimizer.solve()

        self._model.optimization_text = "Retrieving Results"
        self._optimizer.set_results()

        self._model.optimization_text = "DONE"

    def cancel_optimization(self):
        self._optimizer.cancel()
