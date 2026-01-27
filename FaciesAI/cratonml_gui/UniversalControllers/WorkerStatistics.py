import traceback
from dataclasses import dataclass

import numpy as np
from PySide6.QtCore import QRunnable, Slot
from cratonml.calculate.DimensionReduction import get_pca_statistics
from cratonml_gui.utilities import WorkerSignals, Message


@dataclass
class PCAStatisticsResult:
    singular_values: np.ndarray
    explained_variance_ratio: np.ndarray
    sum_explained_variance_ratio: np.ndarray


class WorkerPCAStatistics(QRunnable):
    """Класс для вычисления статистики для каждого компонента в PCA."""

    def __init__(
        self,
        data,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerPCAStatistics, self).__init__()
        self.data = data
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Вычисляет статистику для PCA."""

        try:
            self.signals.message.emit(
                Message(message="Идёт этап вычисления статистики для PCA")
            )
            singular_values, explained_variance_ratio, sum_explained_variance_ratio = (
                get_pca_statistics(self.data)
            )

            self.signals.message.emit(
                Message(message="Вычисление статистики для PCA закончено")
            )
            self.signals.progress.emit(
                (
                    self.start_progress_bar_value,
                    self.end_progress_bar_value,
                )
            )
            result = PCAStatisticsResult(
                singular_values=singular_values,
                explained_variance_ratio=explained_variance_ratio,
                sum_explained_variance_ratio=sum_explained_variance_ratio,
            )
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


#              cratonml_gui/UniversalWidgets/View/CrossPlotWindow.py
