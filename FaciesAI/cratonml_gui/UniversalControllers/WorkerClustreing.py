import traceback
from dataclasses import dataclass
from typing import Any

import numpy as np
from PySide6.QtCore import QRunnable, Slot

from cratonml_gui.utilities import WorkerSignals, Message


@dataclass
class ClusteringResult:
    cluster_list: range or None
    cluster_curve: np.ndarray[Any, np.dtype[Any]] or None
    labels: np.ndarray or None
    cluster: object or None
    n_clusters: int


class WorkerClustering(QRunnable):
    def __init__(
        self,
        data,
        method,
        auto_selection,
        settings,
        start_progress_bar_value,
        end_progress_bar_value,
        data_name="",
        data_number=None,
    ):
        super(WorkerClustering, self).__init__()
        self.data = data
        self.method = method
        self.auto_selection = auto_selection
        self.settings = settings
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.data_name = data_name
        self.data_number = data_number
        if self.data_name:
            self.data_name += ": "
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        cluster_list = None
        cluster_curve = None
        try:
            self.signals.message.emit(
                Message(message=self.data_name + "Начался этап кластеризации данных")
            )
            if self.auto_selection:
                self.signals.message.emit(
                    Message(
                        message=self.data_name
                        + "Идёт этап подбора оптимального количества кластеров"
                    )
                )
                cluster_list, cluster_curve, self.settings["n_clusters"] = (
                    self.method.find_the_best_number_of_clusters(self.data)
                )
                self.signals.progress.emit(
                    (
                        int(self.start_progress_bar_value),
                        int(
                            self.start_progress_bar_value
                            + (
                                self.end_progress_bar_value
                                - self.start_progress_bar_value
                            )
                            // 2
                        ),
                    )
                )

                self.signals.message.emit(
                    Message(
                        message=self.data_name
                        + "Оптимальное количество кластеров: "
                        + str(self.settings["n_clusters"])
                    )
                )
            cluster, labels = self.method.calculate(data=self.data, **self.settings)
            self.signals.progress.emit(
                (
                    int(self.start_progress_bar_value)
                    + (self.end_progress_bar_value - self.start_progress_bar_value)
                    // 2,
                    int(self.end_progress_bar_value),
                )
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Кластеризация проведена успешно")
            )
            if "n_clusters" not in self.settings.keys():
                self.settings["n_clusters"] = self.method.get_number_of_clusters(labels)
            result = ClusteringResult(
                cluster=cluster,
                labels=labels,
                n_clusters=self.settings["n_clusters"],
                cluster_curve=cluster_curve,
                cluster_list=cluster_list,
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Этап кластеризации данных закончен")
            )
            if self.data_number is not None:
                self.signals.result[object, int].emit(result, self.data_number)
            else:
                self.signals.result.emit(result)
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=self.data_name
                    + e.args[0]
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                )
            )
            self.signals.error.emit()
            self.signals.result.emit(None)
