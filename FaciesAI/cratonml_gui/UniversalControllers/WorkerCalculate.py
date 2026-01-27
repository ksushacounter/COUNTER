import traceback
from dataclasses import dataclass

import numpy as np
from cratonml.data import Grid, Well
from cratonml.exceptions.WellExceptions import WellTrajectoryDepthException
from PySide6.QtCore import QRunnable, Slot

from cratonml_gui.utilities import WorkerSignals, Message


@dataclass
class CoordinatesResult:
    coordinates: list or None


@dataclass
class GridValuesInCoordinatesResult:
    grid_values: list


@dataclass
class CurveValuesCalculateResult:
    curve_values: list


@dataclass
class SearchIntersectionPointsResult:
    data: list


class WorkerWellCoordinateCalculate(QRunnable):
    """Класс для вычисления координат в скважине у верхней отбивки, нижней отбивки и посередине."""

    def __init__(
        self,
        connection,
        well_metadata,
        well_info,
        strat_levels_info,
        strat_levels_parameters,
        coords_calculation_parameters,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerWellCoordinateCalculate, self).__init__()
        self.connection = connection
        self.well_metadata = well_metadata
        self.well_info = well_info
        self.strat_levels_info = strat_levels_info
        self.strat_levels_parameters = strat_levels_parameters
        self.coords_calculation_parameters = coords_calculation_parameters
        self.signals = WorkerSignals()
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message="Идет этап получения координат скважин")
            )

            if len(self.well_metadata["well_names"]) == 0:
                self.signals.message.emit(
                    Message(
                        message="Входные данные(скважины) не заданы", is_warning=True
                    )
                )
                self.signals.error.emit()
                self.signals.result.emit(None)
            else:
                coordinates_list = []
                step = (
                    self.end_progress_bar_value - self.start_progress_bar_value
                ) / len(self.well_metadata["well_names"])
                well_cls = Well(self.connection)
                well_ids = self.well_metadata["well_ids"]
                well_names = self.well_metadata["well_names"]
                for well_id, well_name in zip(well_ids, well_names):
                    try:
                        coordinates_dict = well_cls.get_well_coords_by_trajectory(
                            strat_info=self.strat_levels_info[well_id]["strat_levels"],
                            well_id=well_id,
                            well_name=well_name,
                            strat_levels_parameters=self.strat_levels_parameters,
                            coords_calculation_parameters=self.coords_calculation_parameters,
                        )
                        if not coordinates_dict["state"]:
                            self.signals.message.emit(
                                Message(
                                    message=well_name
                                    + ": Не будет использоваться в дальнейших вычислениях. "
                                    "Вероятно, скважина не прошла порог отброса по горизонтальному расстоянию или стратиграфический уровень отсутствует",
                                    is_warning=True,
                                )
                            )
                    except WellTrajectoryDepthException as e:
                        coordinates_dict = {
                            "state": False,
                            "top": np.array([np.nan, np.nan]),
                            "bot": np.array([np.nan, np.nan]),
                            "middle": np.array([np.nan, np.nan]),
                        }
                        self.signals.message.emit(
                            Message(
                                message=well_name
                                + ": "
                                + str(e.args[0])
                                + "\n"
                                + "".join(traceback.format_exception(e)),
                                is_error=True,
                            )
                        )
                        self.signals.error.emit()
                        self.signals.result.emit(None)
                    else:
                        self.signals.message.emit(
                            Message(
                                message="Чтение координаты для скважины {well_name} закончено".format(
                                    well_name=well_name
                                )
                            )
                        )

                    self.signals.progress.emit(
                        (
                            int(self.start_progress_bar_value),
                            int(self.start_progress_bar_value + step),
                        )
                    )
                    self.start_progress_bar_value += step
                    coordinates_list.append(coordinates_dict)

                self.signals.message.emit(
                    Message(message="Этап получения координат скважин закончен")
                )
                self.signals.result.emit(
                    CoordinatesResult(coordinates=coordinates_list)
                )
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


class WorkerOutlineCoordinateCalculate(QRunnable):
    def __init__(
        self, outlines, xx, yy, start_progress_bar_value, end_progress_bar_value
    ):
        super(WorkerOutlineCoordinateCalculate, self).__init__()
        self.outlines = outlines
        self.xx = xx
        self.yy = yy
        self.signals = WorkerSignals()
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value

    @Slot()
    def run(self):
        coordinates_list = []
        try:
            self.signals.message.emit(
                Message(message="Идет этап вычисления координат контуров")
            )
            for i in range(len(self.outlines)):
                mask = np.isnan(self.outlines[i].ravel())
                coordinate_classes = np.array(
                    [self.xx[i].ravel(), self.yy[i].ravel()]
                ).T[np.invert(mask)]
                coordinates_list.extend(coordinate_classes)

            self.signals.progress.emit(
                (self.start_progress_bar_value, self.start_progress_bar_value)
            )
            self.signals.message.emit(
                Message(message="Вычисление координат контуров прошло успешно")
            )
            self.signals.result.emit(CoordinatesResult(coordinates=coordinates_list))
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


class WorkerGridValuesInCoordinatesCalculate(QRunnable):
    """Класс для вычисления значения грида по координатам."""

    def __init__(
        self,
        grid_data,
        grid_xx,
        grid_yy,
        coords,
        well_names,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerGridValuesInCoordinatesCalculate, self).__init__()
        self.grid_data = grid_data
        self.grid_xx = grid_xx
        self.grid_yy = grid_yy
        self.coords = coords
        self.well_names = well_names
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        i = 0
        try:
            grid_values_list = []
            self.signals.message.emit(
                Message(message="Идет этап получения значений с гридов в координатах")
            )
            step = (self.end_progress_bar_value - self.start_progress_bar_value) / len(
                self.coords
            )
            coords_types = ["top", "bot", "middle"]
            for i, well_dict in enumerate(self.coords):
                all_values = {
                    "top": [],
                    "bot": [],
                    "middle": [],
                }
                for data, xx, yy in zip(self.grid_data, self.grid_xx, self.grid_yy):
                    for coords_type in coords_types:
                        all_values[coords_type].append(
                            Grid.get_attribute_values_by_coords(
                                data, xx, yy, well_dict[coords_type]
                            )
                        )
                grid_values = {}
                for coords_type in coords_types:
                    grid_values[coords_type] = np.asarray(all_values[coords_type])[:, 0]
                grid_values_list.append(grid_values)
                self.signals.progress.emit(
                    (
                        int(self.start_progress_bar_value),
                        int(self.start_progress_bar_value + step),
                    )
                )
                self.start_progress_bar_value += step
                self.signals.message.emit(
                    Message(
                        message="Получение значений гридов для скважины {well_name} прошло успешно".format(
                            well_name=self.well_names[i]
                        )
                    )
                )
            result = GridValuesInCoordinatesResult(grid_values=grid_values_list)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=self.well_names[i]
                    + ": "
                    + str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                )
            )
            self.signals.error.emit()
            self.signals.result.emit(None)


class WorkerCurveValuesCalculate(QRunnable):
    """Класс для вычисления значений кривых с помощью метода self.calculator."""

    def __init__(
        self,
        well_curve_list,
        well_names,
        calculator,
        parse_settings,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerCurveValuesCalculate, self).__init__()
        self.well_curve_list = well_curve_list
        self.well_names = well_names
        self.calculator = calculator
        self.parse_settings = parse_settings
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        i = 0
        try:
            all_curve_values = []
            step = (self.end_progress_bar_value - self.start_progress_bar_value) / len(
                self.well_curve_list
            )
            self.signals.message.emit(
                Message(message="Идёт этап вычисления значений кривых")
            )
            for i in range(len(self.well_curve_list)):
                well_values = []
                if isinstance(self.well_curve_list[i].values, type(None)):
                    if np.isinf(self.parse_settings[i]["min_depth"]) and np.isinf(
                        self.parse_settings[i]["max_depth"]
                    ):
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[i]
                                + ": "
                                + "Не участвует в вычислениях - отсутствуют заданные отбивки",
                                is_warning=True,
                            )
                        )
                    elif np.isinf(self.parse_settings[i]["min_depth"]):
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[i]
                                + ": "
                                + "Не участвует в вычислениях - отсутствует заданная верхняя отбивка",
                                is_warning=True,
                            )
                        )
                    elif np.isinf(self.parse_settings[i]["max_depth"]):
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[i]
                                + ": "
                                + "Не участвует в вычислениях - отсутствует заданная нижняя отбивка",
                                is_warning=True,
                            )
                        )
                    else:
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[i]
                                + ": "
                                + "Не участвует в вычислениях - все заданные кривые не имеют значений в данном диапазоне",
                                is_warning=True,
                            )
                        )

                    all_curve_values.append(
                        [np.nan] * len(self.well_curve_list[i].values)
                    )
                    self.signals.progress.emit(
                        (
                            int(self.start_progress_bar_value),
                            int(self.start_progress_bar_value + step),
                        )
                    )
                    self.start_progress_bar_value += step
                else:
                    for j in range(len(self.well_curve_list[i].values)):
                        mask = np.isnan(self.well_curve_list[i].values[j])
                        if np.all(mask):
                            well_values.append(np.nan)
                        else:
                            well_values.append(
                                self.calculator.calculate(
                                    self.well_curve_list[i].values[j][~mask]
                                )
                            )
                    if np.isnan(well_values).all():
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[i]
                                + ": "
                                + "Не участвует в вычислениях - все заданные кривые не имеют значений в данном диапазоне",
                                is_warning=True,
                            )
                        )

                    all_curve_values.append(well_values)
                    self.signals.progress.emit(
                        (
                            int(self.start_progress_bar_value),
                            int(self.start_progress_bar_value + step),
                        )
                    )
                    self.start_progress_bar_value += step

            self.signals.message.emit(
                Message(message="Этап вычисления значений кривых закончен")
            )
            result = CurveValuesCalculateResult(curve_values=all_curve_values)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=self.well_names[i]
                    + ": "
                    + str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                )
            )
            self.signals.error.emit()
            self.signals.result.emit(None)


class WorkerSearchIntersectionPoints(QRunnable):
    def __init__(
        self,
        connection,
        grid_data,
        grid_xx,
        grid_yy,
        coords,
        mask,
        coords_type: str,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerSearchIntersectionPoints, self).__init__()
        self.connection = connection
        self.grid_data = grid_data
        self.grid_xx = grid_xx
        self.grid_yy = grid_yy
        self.coords = coords
        self.mask = mask
        self.coords_type = coords_type
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            result_list = []
            self.signals.message.emit(
                Message(message="Идет этап получения точек пересечения")
            )
            tolerance_x = (self.grid_xx[0][1] - self.grid_xx[0][0]) / 2
            tolerance_y = (self.grid_yy[1][0] - self.grid_yy[0][0]) / 2

            xi = np.array([self.grid_xx.ravel(), self.grid_yy.ravel()]).T[
                np.invert(self.mask)
            ]

            xi_x = xi[:, 0]
            xi_y = xi[:, 1]
            for coordinates in self.coords:
                if type(coordinates) == dict:
                    x, y = coordinates[self.coords_type]
                else:
                    x, y = coordinates
                mask_x = np.abs(xi_x - x) < tolerance_x
                mask_y = np.abs(xi_y - y) < tolerance_y
                indices = np.where(mask_x & mask_y)[0]

                if indices.size > 0:
                    index = indices[0]
                    result_list.append(self.grid_data[index].tolist())
                else:
                    result_list.append([np.nan] * len(self.grid_data[0]))

            self.signals.progress.emit(
                (self.start_progress_bar_value, self.start_progress_bar_value)
            )
            self.signals.message.emit(
                Message(message="Получение точек пересечения прошло успешно")
            )
            result = SearchIntersectionPointsResult(data=result_list)
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
