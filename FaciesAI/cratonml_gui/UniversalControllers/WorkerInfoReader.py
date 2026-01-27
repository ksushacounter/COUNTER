import traceback
from dataclasses import dataclass

from cratonml.data import Grid, Well, Cube, Outline
from PySide6.QtCore import QRunnable, Slot

from cratonml_gui.utilities import WorkerSignals, Message


@dataclass
class InfoReaderResult:
    info: dict


class WorkerGridInfoReader(QRunnable):
    """Класс для чтения метаданных гридов."""

    def __init__(self, connection, start_progress_bar_value, end_progress_bar_value):
        super(WorkerGridInfoReader, self).__init__()
        self.connection = connection
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        grid_info = {}
        try:
            self.signals.message.emit(
                Message(
                    message="Идет этап чтения метаданных гридов",
                    is_message_for_all=True,
                )
            )
            grid = Grid(self.connection)
            grid_info = grid.get_info()
            if grid_info:
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                self.signals.message.emit(
                    Message(
                        message="Чтение метаданных гридов прошло успешно",
                        is_message_for_all=True,
                    )
                )
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                    is_message_for_all=True,
                )
            )
            self.signals.error.emit()
        result = InfoReaderResult(grid_info)
        self.signals.result.emit(result)


class WorkerCubeInfoReader(QRunnable):
    """Класс для чтения метаданных кубов."""

    def __init__(self, connection, start_progress_bar_value, end_progress_bar_value):
        super(WorkerCubeInfoReader, self).__init__()
        self.connection = connection
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        cube_info = {}
        try:
            self.signals.message.emit(
                Message(
                    message="Идет этап чтения метаданных кубов", is_message_for_all=True
                )
            )
            cube = Cube(self.connection)
            cube_info = cube.get_info()
            if cube_info:
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                self.signals.message.emit(
                    Message(
                        message="Чтение метаданных кубов прошло успешно",
                        is_message_for_all=True,
                    )
                )
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                    is_message_for_all=True,
                )
            )
            self.signals.error.emit()
        result = InfoReaderResult(cube_info)
        self.signals.result.emit(result)


class WorkerWellInfoReader(QRunnable):
    """Класс для чтения метаданных скважин."""

    def __init__(self, connection, start_progress_bar_value, end_progress_bar_value):
        super(WorkerWellInfoReader, self).__init__()
        self.connection = connection
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        well_info = {}
        try:
            self.signals.message.emit(
                Message(
                    message="Идет этап чтения метаданных скважин",
                    is_message_for_all=True,
                )
            )
            well = Well(self.connection)
            well_info = well.get_info()
            if well_info:
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                self.signals.message.emit(
                    Message(
                        message="Чтение метаданных скважин прошло успешно",
                        is_message_for_all=True,
                    )
                )
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                    is_message_for_all=True,
                )
            )
            self.signals.error.emit()
        result = InfoReaderResult(well_info)
        self.signals.result.emit(result)


class WorkerAllStratLevelsInfoReader(QRunnable):
    """Класс для чтения стратиграфических уровней."""

    def __init__(self, connection, start_progress_bar_value, end_progress_bar_value):
        super(WorkerAllStratLevelsInfoReader, self).__init__()
        self.connection = connection
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Возвращает словарь, где ключ - имя стратиграфического уровня, а значение - идентификатор уровня."""

        all_strat_levels_info = {}
        try:
            self.signals.message.emit(
                Message(message="Идёт этап чтения отбивок", is_message_for_all=True)
            )
            well = Well(self.connection)
            all_strat_levels_info = well.get_all_strat_levels_dict()
            if all_strat_levels_info:
                self.signals.message.emit(
                    Message(
                        message="Чтение отбивок прошло успешно", is_message_for_all=True
                    )
                )
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                    is_message_for_all=True,
                )
            )
            self.signals.error.emit()
        result = InfoReaderResult(info=all_strat_levels_info)
        self.signals.result.emit(result)


class WorkerCurveDisplayPropertiesReader(QRunnable):
    """Класс для чтения метаданных гридов."""

    def __init__(self, connection, start_progress_bar_value, end_progress_bar_value):
        super(WorkerCurveDisplayPropertiesReader, self).__init__()
        self.connection = connection
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        display_properties = {}
        try:
            self.signals.message.emit(
                Message(
                    message="Идет этап чтения метаданных тэгов кривых",
                    is_message_for_all=True,
                )
            )
            well = Well(self.connection)
            display_properties = well.get_curve_display_properties()

            if display_properties:
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                self.signals.message.emit(
                    Message(
                        message="Чтение метаданных тэгов кривых прошло успешно",
                        is_message_for_all=True,
                    )
                )
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                    is_message_for_all=True,
                )
            )
            self.signals.error.emit()
        result = InfoReaderResult(info=display_properties)
        self.signals.result.emit(result)


class WorkerCurvesInfoReader(QRunnable):
    """Класс для чтения метаданных кривых."""

    def __init__(
        self, connection, well_ids, start_progress_bar_value, end_progress_bar_value
    ):
        super(WorkerCurvesInfoReader, self).__init__()
        self.connection = connection
        self.well_ids = well_ids
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message="Идет этап чтения метаданных кривых")
            )
            well = Well(self.connection)
            curves_info = well.get_curves_info(well_ids=self.well_ids)
            if curves_info:
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                self.signals.message.emit(
                    Message(message="Чтение метаданных кривых прошло успешно")
                )
                result = InfoReaderResult(curves_info)
                self.signals.result.emit(result)
            else:
                if not self.well_ids:
                    self.signals.message.emit(
                        Message(
                            message="Скважины не заданы.",
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


class WorkerStratLevelsInfoReader(QRunnable):
    """Класс для чтения метаданных стратиграфических уровней."""

    def __init__(
        self,
        connection,
        well_ids,
        all_strat_levels_info,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(WorkerStratLevelsInfoReader, self).__init__()
        self.connection = connection
        self.well_ids = well_ids
        self.all_strat_levels_info = all_strat_levels_info
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.message.emit(
                Message(message="Идет этап чтения метаданных стратиграфических уровней")
            )
            well = Well(self.connection)
            strat_levels_info = well.get_strat_levels_info(
                well_ids=self.well_ids, all_strat_levels_info=self.all_strat_levels_info
            )
            if strat_levels_info:
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                self.signals.message.emit(
                    Message(
                        message="Чтение метаданных стратиграфических уровней прошло успешно"
                    )
                )
                result = InfoReaderResult(strat_levels_info)
                self.signals.result.emit(result)
            else:
                if not self.well_ids:
                    self.signals.message.emit(
                        Message(
                            message="Скважины не заданы.",
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


class WorkerOutlineInfoReader(QRunnable):
    def __init__(self, connection, start_progress_bar_value, end_progress_bar_value):
        super(WorkerOutlineInfoReader, self).__init__()
        self.connection = connection
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        outline_info = {}
        try:
            self.signals.message.emit(
                Message(
                    message="Идет этап чтения метаданных контуров",
                    is_message_for_all=True,
                )
            )
            outline = Outline(self.connection)
            outline_info = outline.get_info()
            if outline_info:
                self.signals.progress.emit(
                    (self.start_progress_bar_value, self.end_progress_bar_value)
                )
                self.signals.message.emit(
                    Message(
                        message="Чтение метаданных контуров прошло успешно",
                        is_message_for_all=True,
                    )
                )
        except Exception as e:
            self.signals.message.emit(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                    is_message_for_all=True,
                )
            )
            self.signals.error.emit()
        result = InfoReaderResult(outline_info)
        self.signals.result.emit(result)
