import traceback
from dataclasses import dataclass

import numpy as np
from PySide6.QtCore import QRunnable, Slot

from cratonml_gui.utilities import WorkerSignals, Message


@dataclass
class RegressionCoefficientsResult:
    a: np.ndarray or None
    b: np.ndarray or float or None


class WorkerRegressionCoefficients(QRunnable):
    """Класс вычисляющий коэффициенты регрессии."""

    def __init__(
        self,
        x_train,
        y_train,
        method,
        start_progress_bar_value=0,
        end_progress_bar_value=0,
    ):
        super(WorkerRegressionCoefficients, self).__init__()
        self.x_train = x_train
        self.y_train = y_train
        self.method = method
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Выполняет обучение регрессионной модели и получает коэффициенты регрессии."""

        try:
            self.signals.message.emit(
                Message(message=f"Идёт этап обучения модели регрессии")
            )
            model = self.method.get_model(x_train=self.x_train, y_train=self.y_train)
            self.signals.progress.emit(
                (
                    self.start_progress_bar_value,
                    self.start_progress_bar_value
                    + (self.end_progress_bar_value - self.start_progress_bar_value)
                    // 2,
                )
            )
            self.signals.message.emit(
                Message(message=f"Модель регрессии обучена успешно")
            )
            self.signals.message.emit(
                Message(message=f"Идёт этап получения коэффициентов регрессии")
            )
            a, b = self.method.get_coeffs(model)
            self.signals.progress.emit(
                (
                    self.start_progress_bar_value
                    + (self.end_progress_bar_value - self.start_progress_bar_value)
                    // 2,
                    self.end_progress_bar_value,
                )
            )
            self.signals.message.emit(
                Message(message=f"Коэффициенты регрессии получены")
            )
            result = RegressionCoefficientsResult(a=a, b=b)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                )
            )
            self.signals.error.emit()
            self.signals.result.emit(None)
