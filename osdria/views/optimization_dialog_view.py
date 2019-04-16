from PySide2.QtCore import Qt, QObject, QSize, QModelIndex, Signal
from PySide2.QtWidgets import QDialog, QStyledItemDelegate, QPushButton, QWidget, QStyle, QHeaderView

from views.optimization_dialog_view_ui import Ui_OptimizationDialog


class OptimizationDialogView(QDialog):
    """Optimization Dialog View"""
    dialog_shown = Signal()

    def __init__(self, dialog_model, dialog_controller):
        settings = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        super(OptimizationDialogView, self).__init__(None, settings)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._model = dialog_model
        self._ctrl = dialog_controller
        self._ui = Ui_OptimizationDialog()
        self._ui.setupUi(self)

        """connect widgets to controller"""
        self.dialog_shown.connect(self._ctrl.run_optimization)
        self._ui.cancel_button.clicked.connect(self.reject)
        self.rejected.connect(self._ctrl.cancel_optimization)

        """listen for model event signals"""
        self._model.text_changed.connect(self._ui.information_text.setText)

        """initialize view"""
        self._model.optimization_text = "Optimization Started"

    def on_text_changed(self, text):
        """change text of label"""
        self._ui.information_text.setText(text)
        if text == "DONE":
            self.accept()

    def exec_(self, *args, **kwargs):
        self.dialog_shown.emit()
        return super().exec_(*args, **kwargs)

    def keyPressEvent(self, event):
        """prevent dialog closing with enter or return key"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            return
        super().keyPressEvent(event)
