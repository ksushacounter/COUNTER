import traceback
from dataclasses import dataclass

import numpy as np
from cratonml.calculate.Prepare import drop_nan
from cratonml.data import Grid
from PySide6.QtCore import QRunnable, Slot

from cratonml_gui.utilities import WorkerSignals, Message

RANDOM_SEED = 52


@dataclass
class PreparerResult:
    data: np.ndarray
    mask: np.ndarray
    mask_curve: np.ndarray or None = None


@dataclass
class GridMergingResult:
    data: np.ndarray
    xx: np.ndarray
    yy: np.ndarray


@dataclass
class SamplesPreparerResult:
    train_data: np.ndarray
    test_data: np.ndarray
    train_labels: np.ndarray
    test_labels: np.ndarray
    attributes_data: np.ndarray


class WorkerGridMerging(QRunnable):
    """Класс для парсинга списка гридов в numpy массив."""

    def __init__(self, grid_list, start_progress_bar_value, end_progress_bar_value):
        super(WorkerGridMerging, self).__init__()
        self.grid_list = grid_list
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message=f"Начался этап объединения сеток")
            )
            data, xx, yy = Grid.parse_to_numpy(self.grid_list)
            self.signals.progress.emit(
                (self.start_progress_bar_value, self.end_progress_bar_value)
            )
            self.signals.message.emit(
                Message(message=f"Объединение сеток прошло успешно")
            )
            result = GridMergingResult(data, xx, yy)
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


class WorkerPreparer(QRunnable):
    def __init__(
        self,
        data,
        settings,
        start_progress_bar_value,
        end_progress_bar_value,
        data_name="",
        data_number=None,
        isCurves=False,
    ):
        super(WorkerPreparer, self).__init__()
        self.data = data
        self.settings = settings
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.isCurves = isCurves
        self.data_name = data_name
        self.data_number = data_number
        if self.data_name:
            self.data_name += ": "
        self.signals = WorkerSignals()

    def __run_scaler(self):
        self.signals.message.emit(
            Message(message=self.data_name + "Идёт этап нормализации данных")
        )
        self.data_prepared, _ = self.settings["scaler"](data=self.data_prepared)
        self.signals.progress.emit(
            (
                int(self.start_progress_bar_value),
                int(self.start_progress_bar_value + self.pb_value_for_operation),
            )
        )
        self.start_progress_bar_value += self.pb_value_for_operation
        self.signals.message.emit(
            Message(message=self.data_name + "Нормализация данных проведена успешно")
        )

    def __run_outliers(self):
        self.signals.message.emit(
            Message(message=self.data_name + "Идёт этап поиска выбросов")
        )
        self.data_prepared, mask_prepared = self.settings["outliers"](
            data=self.data_prepared
        )
        self.mask[self.mask == False] = ~mask_prepared
        self.signals.progress.emit(
            (
                int(self.start_progress_bar_value),
                int(self.start_progress_bar_value + self.pb_value_for_operation),
            )
        )
        self.start_progress_bar_value += self.pb_value_for_operation
        self.signals.message.emit(
            Message(message=self.data_name + "Поиск выбросов проведен успешно")
        )

    def __run_dimension_reduction(self):
        self.signals.message.emit(
            Message(message=self.data_name + "Идёт этап понижения размерности")
        )
        self.data_prepared = self.settings["dimension_reduction"](
            data=self.data_prepared, **self.settings["dimension_reduction_params"]
        )
        self.signals.progress.emit(
            (
                int(self.start_progress_bar_value),
                int(self.start_progress_bar_value + self.pb_value_for_operation),
            )
        )
        self.start_progress_bar_value += self.pb_value_for_operation
        self.signals.message.emit(
            Message(
                message=self.data_name + "Этап понижения размерности проведен успешно"
            )
        )

    def __run_balancing(self):
        self.signals.message.emit(
            Message(message=self.data_name + "Идёт этап балансировки")
        )
        self.data_prepared = self.settings["balancing"](
            data=self.data_prepared, **self.settings["balancing_params"]
        )
        self.signals.progress.emit(
            (
                int(self.start_progress_bar_value),
                int(self.start_progress_bar_value + self.pb_value_for_operation),
            )
        )
        self.start_progress_bar_value += self.pb_value_for_operation
        self.signals.message.emit(
            Message(message=self.data_name + "Этап балансировки проведен успешно")
        )

    @Slot()
    def run(self):
        mask_curve = None
        self.data_prepared = None
        self.mask = None
        try:
            self.signals.message.emit(
                Message(message=self.data_name + "Начался этап подготовки данных")
            )
            self.n_operations = 1 + sum(
                [
                    self.settings["scaler"] != False,
                    self.settings["outliers"] != False,
                    self.settings["dimension_reduction"] != False,
                    self.settings["balancing"] != False,
                ]
            )
            self.pb_value_for_operation = (
                self.end_progress_bar_value - self.start_progress_bar_value
            ) / self.n_operations
            if self.isCurves:
                mask_curve = np.all(np.isnan(self.data), axis=0)
                self.data = self.data[:, ~mask_curve]
            self.signals.message.emit(
                Message(message=self.data_name + "Идёт этап построения маски")
            )
            self.data_prepared, self.mask = drop_nan(data=self.data)
            if self.data_prepared.size == 0:
                self.signals.message.emit(
                    Message(
                        message=self.data_name
                        + "Все строки данных имеют значение None",
                        is_warning=True,
                    )
                )
                self.signals.error.emit()
                self.signals.result.emit(None)
                return

            self.signals.progress.emit(
                (
                    int(self.start_progress_bar_value),
                    int(self.start_progress_bar_value + self.pb_value_for_operation),
                )
            )
            self.start_progress_bar_value += self.pb_value_for_operation

            self.signals.message.emit(
                Message(message=self.data_name + "Маска построена успешно")
            )
            if self.settings["scaler"]:
                self.__run_scaler()
            if self.settings["outliers"]:
                self.__run_outliers()
            if self.settings["dimension_reduction"]:
                self.__run_dimension_reduction()
            if self.settings["balancing"]:
                self.__run_balancing()
            self.signals.progress.emit(
                (int(self.start_progress_bar_value), int(self.end_progress_bar_value))
            )
            result = PreparerResult(
                data=self.data_prepared, mask=self.mask, mask_curve=mask_curve
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Этап подготовки данных закончен")
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


class WorkerSamplesPreparer(QRunnable):
    def __init__(
        self,
        data,
        classes,
        test_percent,
        attributes_data,
        scaler_func,
        balancing,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerSamplesPreparer, self).__init__()
        self.data = data
        self.classes = classes
        self.test_percent = test_percent
        self.attributes_data = attributes_data
        self.scaler_func = scaler_func
        self.balancing = balancing
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message=f"Начался этап разделения данных на выборки")
            )
            indexes = np.arange(len(self.classes))

            test_size = min(
                max(int(len(indexes) * self.test_percent / 100), 1), len(indexes) - 1
            )
            train_size = len(indexes) - test_size

            np.random.seed(RANDOM_SEED)
            train_name_list = np.random.choice(indexes, size=train_size, replace=False)
            test_name_list = [item for item in indexes if item not in train_name_list]

            test_labels = np.array(self.classes)[test_name_list]
            train_labels = np.array(self.classes)[train_name_list]
            data_test = np.array(self.data)[test_name_list]
            data_train = np.array(self.data)[train_name_list]
            self.signals.message.emit(
                Message(message=f"Этап разделения данных на выборки прошел успешно")
            )
            attributes_data_scaled = self.attributes_data.copy()
            if self.scaler_func:
                self.signals.message.emit(
                    Message(message=f"Идёт этап нормализации данных")
                )
                attributes_data_scaled, scaler = self.scaler_func(self.attributes_data)
                data_test, _ = self.scaler_func(data_test, scaler)
                data_train, _ = self.scaler_func(data_train, scaler)
                self.signals.message.emit(
                    Message(message=f"Нормализация данных проведена успешно")
                )
            if self.balancing:
                self.signals.message.emit(Message(message=f"Идёт этап балансировки"))
                data_train, train_labels = self.balancing(data_train, train_labels)
                self.signals.message.emit(
                    Message(message=f"Балансировка проведена успешно")
                )
            self.signals.message.emit(
                Message(message=f"Этап подготовки данных закончен")
            )
            result = SamplesPreparerResult(
                train_data=data_train,
                test_data=data_test,
                train_labels=train_labels,
                test_labels=test_labels,
                attributes_data=attributes_data_scaled,
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
