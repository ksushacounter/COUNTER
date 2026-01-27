import traceback
from dataclasses import dataclass

import numpy as np
from PySide6.QtCore import QRunnable, Slot

from cratonml_gui.utilities import Message, WorkerSignals


@dataclass
class ClassificationResult:
    model: object or None
    prediction: np.ndarray or None


@dataclass
class PredictResult:
    prediction: np.ndarray or None


class WorkerClassification(QRunnable):
    def __init__(
        self,
        x_train,
        y_train,
        x_test,
        method,
        settings,
        start_progress_bar_value=0,
        end_progress_bar_value=0,
    ):
        super(WorkerClassification, self).__init__()
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.method = method
        self.settings = settings
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value

        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message=f"Начался этап классификации данных")
            )
            self.signals.message.emit(Message(message=f"Идёт этап обучения модели"))
            model = self.method.get_model(
                x_train=self.x_train, y_train=self.y_train, **self.settings
            )
            self.signals.progress.emit(
                (
                    self.start_progress_bar_value,
                    self.start_progress_bar_value
                    + (self.end_progress_bar_value - self.start_progress_bar_value)
                    // 2,
                )
            )
            self.signals.message.emit(Message(message=f"Модель обучена успешно"))
            self.signals.message.emit(Message(message=f"Идёт этап прогнозирования"))
            prediction = self.method.predict(model=model, x_test=self.x_test)
            self.signals.message.emit(
                Message(message=f"Этап прогнозирование прошёл успешно")
            )

            self.signals.progress.emit(
                (
                    self.start_progress_bar_value
                    + (self.end_progress_bar_value - self.start_progress_bar_value)
                    // 2,
                    self.end_progress_bar_value,
                )
            )
            result = ClassificationResult(model=model, prediction=prediction)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=e.args[0] + "\n" + "".join(traceback.format_exception(e)),
                    is_error=True,
                )
            )
            self.signals.error.emit()
            self.signals.result.emit(None)


class WorkerPredict(QRunnable):
    def __init__(
        self, data, method, model, start_progress_bar_value=0, end_progress_bar_value=0
    ):
        super(WorkerPredict, self).__init__()
        self.data = data
        self.method = method
        self.model = model
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value

        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(Message(message=f"Идёт этап прогнозирования"))
            prediction = self.method.predict(model=self.model, x_test=self.data)
            self.signals.progress.emit(
                (self.start_progress_bar_value, self.end_progress_bar_value)
            )
            self.signals.message.emit(
                Message(message=f"Этап прогнозирование прошёл успешно")
            )
            result = PredictResult(prediction=prediction)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=e.args[0] + "\n" + "".join(traceback.format_exception(e)),
                    is_error=True,
                )
            )
            self.signals.error.emit()
            self.signals.result.emit(None)
