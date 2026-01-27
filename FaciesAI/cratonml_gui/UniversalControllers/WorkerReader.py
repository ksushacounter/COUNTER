import traceback
from dataclasses import dataclass
from typing import List

import numpy as np
from cratonml.data import Grid, Well, Cube, Outline
from PySide6.QtCore import QRunnable, Slot
from cratonml.exceptions.DataExceptions import EmptyInputDataException
from cratonml.exceptions.WellExceptions import WellEmptyCurvesException

from cratonml_gui.utilities import WorkerSignals, Message


@dataclass
class GridReaderResult:
    data: np.ndarray
    xx: np.ndarray
    yy: np.ndarray
    grid_list: List[Grid] = None


@dataclass
class CubeReaderResult:
    grid_values: np.ndarray
    xx: np.ndarray
    yy: np.ndarray
    blank_code: float


@dataclass
class WellReaderResult:
    values: np.ndarray or None
    depths: np.ndarray or None


@dataclass
class CurvesReaderResult:
    curves: list


@dataclass
class OutlineReaderResult:
    outlines: list
    xx: list
    yy: list
    outline_list: list
    outline_ids: list


class WorkerGridReader(QRunnable):
    """Класс для чтения гридов."""

    def __init__(
        self,
        connection,
        settings,
        start_progress_bar_value,
        end_progress_bar_value,
        grid_unification=True,
    ):
        super(WorkerGridReader, self).__init__()
        self.connection = connection
        self.settings = settings
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.grid_unification = grid_unification
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Читает грид и парсит его в numpy массив."""

        try:
            self.signals.message.emit(Message(message="Идёт этап чтения гридов"))
            grid_cls = Grid(self.connection)
            grid_list = grid_cls.read(**self.settings)
            if grid_list:
                self.signals.message.emit(
                    Message(message="Чтение гридов прошло успешно")
                )
                self.signals.progress.emit(
                    (
                        self.start_progress_bar_value,
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2,
                    )
                )
                self.signals.message.emit(Message(message="Идёт этап парсинга гридов"))

                if self.grid_unification:
                    data, xx, yy = grid_cls.parse_to_numpy(grid_list)
                else:
                    data = []
                    xx = []
                    yy = []
                    for grid in grid_list:
                        data_, xx_, yy_ = grid_cls.parse_to_numpy([grid])
                        data.append(data_)
                        xx.append(xx_)
                        yy.append(yy_)

                self.signals.message.emit(
                    Message(message="Парсинг гридов прошел успешно")
                )
                self.signals.progress.emit(
                    (
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2,
                        self.end_progress_bar_value,
                    )
                )
                result = GridReaderResult(data, xx, yy, grid_list)
                self.signals.result.emit(result)
            else:
                self.signals.error.emit()
                self.signals.result.emit(None)
        except EmptyInputDataException:
            self.signals.message.emit(
                Message(message="Входные данные(гриды) не заданы", is_warning=True)
            )
            self.signals.error.emit()
            self.signals.result.emit(None)
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


class WorkerCubeReader(QRunnable):
    def __init__(
        self,
        connection,
        cube_parsing_properties,
        cube_properties,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerCubeReader, self).__init__()
        self.connection = connection
        self.cube_parsing_properties = cube_parsing_properties
        self.cube_properties = cube_properties
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(Message(message="Идёт этап чтения куба"))
            if self.cube_properties is None:
                self.signals.message.emit(
                    Message(message="Входные данные(куб) не заданы", is_warning=True)
                )
                self.signals.error.emit()
                self.signals.result.emit(None)
            else:
                cube = Cube(self.connection)
                data_cube = cube.read(**self.cube_properties)
                if data_cube.data.size != 0:
                    self.signals.message.emit(
                        Message(message="Чтение куба прошло успешно")
                    )
                    self.signals.progress.emit(
                        (
                            self.start_progress_bar_value,
                            self.start_progress_bar_value
                            + (
                                self.end_progress_bar_value
                                - self.start_progress_bar_value
                            )
                            // 2,
                        )
                    )
                    self.signals.message.emit(
                        Message(message="Идёт этап парсинга куба")
                    )

                    grid_values, xx, yy, blank_code = cube.parse_to_numpy(
                        cube=data_cube, cube_props=self.cube_parsing_properties
                    )
                    self.signals.message.emit(
                        Message(message="Парсинг куба прошел успешно")
                    )
                    self.signals.progress.emit(
                        (
                            self.start_progress_bar_value
                            + (
                                self.end_progress_bar_value
                                - self.start_progress_bar_value
                            )
                            // 2,
                            self.end_progress_bar_value,
                        )
                    )
                    result = CubeReaderResult(grid_values, xx, yy, blank_code)
                    self.signals.result.emit(result)
                else:
                    if self.cube_properties["cube_id"]:
                        if data_cube.samples_count != 0:
                            self.signals.message.emit(
                                Message(
                                    message="У куба нет значений в данном диапазоне",
                                    is_warning=True,
                                )
                            )
                        self.signals.error.emit()
                        self.signals.result.emit(None)
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


class WorkerWellReader(QRunnable):
    """Класс для чтения скважин."""

    def __init__(
        self,
        connection,
        settings,
        parse_settings,
        well_names,
        start_progress_bar_value,
        end_progress_bar_value,
        multiple_wells=False,
        parse_without_interpolation=False,
    ):
        super(WorkerWellReader, self).__init__()
        self.connection = connection
        self.settings = settings
        self.parse_settings = parse_settings
        self.well_names = well_names
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.multiple_wells = multiple_wells
        self.parse_without_interpolation = parse_without_interpolation
        self.signals = WorkerSignals()

    def emit_error(self):
        if self.multiple_wells or len(self.settings) == 0:
            self.signals.error.emit()
            self.signals.result.emit(None)
        else:
            for data_number in range(len(self.settings)):
                self.signals.error.emit()
                self.signals.result.emit(None)

    @Slot()
    def run(self):
        """
        Читает заданные кривые для каждой скважины(данные для чтения лежат в параметре settings).
        Преобразовывает их значения в numpy массив(если parse_without_interpolation=False) или список numpy массивов(если parse_without_interpolation=True).
        Если parse_without_interpolation=True, то скважины парсятся без интерполяции.
        Если multiple_wells=False, то сигнал с результатом отправляется после парсинга каждой скважины, иначе сигнал отправляется после парсинга всех скважин.
        """

        try:
            self.signals.message.emit(Message(message="Идёт этап чтения кривых"))
            if len(self.settings) == 0:
                self.signals.message.emit(
                    Message(
                        message="Входные данные(скважины) не заданы", is_warning=True
                    )
                )
                self.emit_error()
            elif np.all(
                [len(setting["well_curve_types"]) == 0 for setting in self.settings]
            ):
                self.signals.message.emit(
                    Message(message="Входные данные(кривые) не заданы", is_warning=True)
                )
                self.emit_error()
            else:
                result_list = []
                step = (
                    self.end_progress_bar_value - self.start_progress_bar_value
                ) / len(self.settings)
                for data_number in range(len(self.settings)):
                    values = None
                    depths = None
                    try:
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[data_number]
                                + ": Идёт этап чтения кривых из скважины",
                            )
                        )
                        well = Well(self.connection)
                        curves_list = well.read_by_types(**self.settings[data_number])

                        if curves_list:
                            self.signals.message.emit(
                                Message(
                                    message=self.well_names[data_number]
                                    + ": Чтение кривых прошло успешно",
                                )
                            )
                            self.signals.message.emit(
                                Message(
                                    message=self.well_names[data_number]
                                    + ": Идёт этап парсинга кривых",
                                )
                            )
                            if self.parse_without_interpolation:
                                if not np.all(
                                    [
                                        (
                                            np.isnan(curve.point_values).all()
                                            if curve is not None
                                            else curve is None
                                        )
                                        for curve in curves_list
                                    ]
                                ):
                                    values, depths = (
                                        well.parse_to_numpy_without_interpolation(
                                            curves_list,
                                            **self.parse_settings[data_number]
                                        )
                                    )
                            else:
                                values, depths = well.parse_to_numpy(
                                    curves_list, **self.parse_settings[data_number]
                                )
                            self.signals.message.emit(
                                Message(
                                    message=self.well_names[data_number]
                                    + ": Парсинг кривых прошел успешно",
                                )
                            )
                            self.signals.progress.emit(
                                (
                                    int(self.start_progress_bar_value),
                                    int(self.start_progress_bar_value + step),
                                )
                            )
                            self.start_progress_bar_value += step
                        else:
                            self.signals.message.emit(
                                Message(
                                    message=self.well_names[data_number]
                                    + ": "
                                    + "Выбранных кривых нет в скважине или они не видимы",
                                    is_warning=True,
                                )
                            )
                            self.signals.error.emit()
                            self.signals.result.emit(None)
                            continue
                    except WellEmptyCurvesException:
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[data_number]
                                + ": "
                                + "Входные данные(кривые) не заданы",
                                is_warning=True,
                            )
                        )
                        self.signals.error.emit()
                        self.signals.result.emit(None)
                    except Exception as e:
                        self.signals.message.emit(
                            Message(
                                message=self.well_names[data_number]
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
                        result_i = WellReaderResult(values=values, depths=depths)
                        if self.multiple_wells:
                            result_list.append(result_i)
                        else:
                            self.signals.result[object, int].emit(result_i, data_number)
                if self.multiple_wells:
                    self.signals.result.emit(result_list)
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


class WorkerCurveReader(QRunnable):
    def __init__(
        self, connection, settings, start_progress_bar_value, end_progress_bar_value
    ):
        super(WorkerCurveReader, self).__init__()
        self.connection = connection
        self.settings = settings
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(Message(message="Идёт этап чтения кривых"))
            if len(self.settings) == 0:
                self.signals.message.emit(
                    Message(message="Скважины не заданы", is_warning=True)
                )
                self.signals.error.emit()
                self.signals.result.emit(None)
            else:
                well = Well(self.connection)
                curves = []
                for setting in self.settings:
                    curves.append(well.read_curve(**setting))
                self.signals.message.emit(
                    Message(message="Чтения кривых прошло успешно.")
                )
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                result = CurvesReaderResult(curves)
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


class WorkerOutlineReader(QRunnable):
    def __init__(
        self, connection, settings, start_progress_bar_value, end_progress_bar_value
    ):
        super(WorkerOutlineReader, self).__init__()
        self.connection = connection
        self.settings = settings
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(Message(message="Идёт этап чтения контуров"))
            outline = Outline(self.connection)
            outline_list, outline_ids = outline.read(**self.settings)
            if outline_list:
                self.signals.message.emit(
                    Message(message="Чтение контуров прошло успешно")
                )
                self.signals.progress.emit(
                    (
                        self.start_progress_bar_value,
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2,
                    )
                )

                self.signals.message.emit(
                    Message(message="Идёт этап парсинга контуров")
                )

                outlines, xx, yy = outline.parse_to_numpy(outline_list)

                self.signals.message.emit(
                    Message(message="Парсинг контуров прошел успешно")
                )
                self.signals.progress.emit(
                    (
                        self.start_progress_bar_value
                        + (self.end_progress_bar_value - self.start_progress_bar_value)
                        // 2,
                        self.end_progress_bar_value,
                    )
                )
                result = OutlineReaderResult(
                    outlines=outlines,
                    xx=xx,
                    yy=yy,
                    outline_list=outline_list,
                    outline_ids=outline_ids,
                )
                self.signals.result.emit(result)
            else:
                self.signals.error.emit()
                self.signals.result.emit(None)
        except EmptyInputDataException:
            self.signals.message.emit(
                Message(message="Входные данные(контуры) не заданы", is_warning=True)
            )
            self.signals.error.emit()
            self.signals.result.emit(None)
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
