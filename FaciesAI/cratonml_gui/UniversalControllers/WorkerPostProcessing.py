import traceback
import numpy as np
from PySide6.QtCore import QRunnable, Slot
from dataclasses import dataclass
from cratonml.calculate.PostProcessing import (
    fill_with_value_by_mask,
    curve_peaks_processing,
)

from cratonml_gui.utilities import Message, WorkerSignals

GRID_NAN_VALUE = 1.70141e38
CURVE_NAN_VALUE = -999.25


@dataclass
class GridWorkerPostProcessingResult:
    filled_data: np.ndarray or None


@dataclass
class WellWorkerPostProcessingResult:
    filled_data: np.ndarray or None
    data_number: int or None = None


class GridWorkerPostProcessing(QRunnable):
    def __init__(self, data, mask, x, start_progress_bar_value, end_progress_bar_value):
        super(GridWorkerPostProcessing, self).__init__()
        self.data = data
        self.mask = mask
        self.x = x
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message="Идет этап восстановления значений грида по маске")
            )
            filled_data = fill_with_value_by_mask(
                data=self.data, mask=self.mask, blank_code=GRID_NAN_VALUE
            )
            self.signals.progress.emit(
                (
                    int(self.start_progress_bar_value),
                    int(
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2
                    ),
                )
            )
            self.signals.message.emit(Message(message="Восстановление прошло успешно"))
            self.signals.progress.emit(
                (
                    int(
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2
                    ),
                    int(self.end_progress_bar_value),
                )
            )
            result = GridWorkerPostProcessingResult(filled_data=filled_data)
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


class WellWorkerPostProcessing(QRunnable):
    def __init__(
        self,
        values,
        mask,
        depths,
        minimal_width_in_meter,
        start_progress_bar_value,
        end_progress_bar_value,
        data_name="",
        data_number=None,
    ):
        super(WellWorkerPostProcessing, self).__init__()
        self.values = values
        self.mask = mask
        self.depths = depths
        self.minimal_width_in_meter = minimal_width_in_meter
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.data_name = data_name
        self.data_number = data_number
        if self.data_name:
            self.data_name += ": "
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message=self.data_name + "Идет этап обработки кривой")
            )
            curve_values = curve_peaks_processing(
                curve=self.values,
                depth=self.depths,
                minimal_width_in_meter=self.minimal_width_in_meter,
            )
            self.signals.progress.emit(
                (
                    int(self.start_progress_bar_value),
                    int(
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2
                    ),
                )
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Обработка кривой прошла успешно")
            )

            self.signals.message.emit(
                Message(
                    message=self.data_name
                    + "Идет этап восстановления значений кривой по маске"
                )
            )
            filled_data = fill_with_value_by_mask(
                data=curve_values, mask=self.mask, blank_code=CURVE_NAN_VALUE
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Восстановление прошло успешно")
            )
            self.signals.progress.emit(
                (
                    int(
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2
                    ),
                    int(self.end_progress_bar_value),
                )
            )
            result = WellWorkerPostProcessingResult(
                filled_data=filled_data, data_number=self.data_number
            )
            if self.data_number is not None:
                self.signals.result[object, int].emit(result, self.data_number)
            else:
                self.signals.result.emit(result)
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=self.data_name
                    + str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                )
            )
            self.signals.error.emit()
            self.signals.result.emit(None)
