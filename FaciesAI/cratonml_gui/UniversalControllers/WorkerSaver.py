import traceback

from cratonml.data import Grid, Well
from PySide6.QtCore import QRunnable, Slot

from cratonml_gui.utilities import WorkerSignals, Message

GRID_NAN_VALUE = 1.70141e38


class GridWorkerSaver(QRunnable):
    """Класс для сохранения грида"""

    def __init__(
        self,
        connection,
        data,
        x,
        y,
        name,
        start_progress_bar_value,
        end_progress_bar_value,
    ):
        super(GridWorkerSaver, self).__init__()
        self.connection = connection
        self.data = data
        self.x = x
        self.y = y
        self.name = name
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Преобразовывает numpy массив в грид и сохраняет его в Desmana."""

        try:
            progress_bar_step = (
                self.end_progress_bar_value - self.start_progress_bar_value
            ) // 2
            self.signals.message.emit(
                Message(message="Идет этап преобразования массива в грид")
            )
            grid = Grid(self.connection)
            grid_to_save = grid.numpy_to_grid(
                data=self.data, x=self.x, y=self.y, blank_code=GRID_NAN_VALUE
            )

            self.signals.progress.emit(
                (
                    self.start_progress_bar_value,
                    self.start_progress_bar_value + progress_bar_step,
                )
            )
            self.signals.message.emit(Message(message="Преобразование прошло успешно"))
            self.signals.message.emit(Message(message="Идет этап сохранения грида"))

            grid.save(self.name, grid_to_save)
            self.signals.progress.emit(
                (
                    self.start_progress_bar_value + progress_bar_step,
                    self.end_progress_bar_value,
                )
            )
            self.signals.message.emit(Message(message="Этап сохранения грида закончен"))
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


class WellWorkerSaver(QRunnable):
    """Класс для сохранения кривой в скважину"""

    def __init__(
        self,
        connection,
        data,
        depths,
        curve_name,
        curve_type,
        well_id,
        start_progress_bar_value,
        end_progress_bar_value,
        data_name="",
    ):
        super(WellWorkerSaver, self).__init__()
        self.connection = connection
        self.data = data
        self.depths = depths
        self.curve_name = curve_name
        self.curve_type = curve_type
        self.well_id = well_id
        self.start_progress_bar_value = start_progress_bar_value
        self.end_progress_bar_value = end_progress_bar_value
        self.data_name = data_name
        if self.data_name:
            self.data_name += ": "
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Преобразовывает numpy массив в кривую и сохраняет его в GISWell."""

        try:
            progress_bar_step = (
                self.end_progress_bar_value - self.start_progress_bar_value
            ) // 2
            self.signals.message.emit(
                Message(
                    message=self.data_name + "Идет этап преобразования массива в кривую"
                )
            )
            well = Well(self.connection)
            well_curve_to_save = well.numpy_to_curve(
                values=self.data,
                depths=self.depths,
                curve_name=self.curve_name,
                curve_type=self.curve_type,
            )
            self.signals.progress.emit(
                (
                    self.start_progress_bar_value,
                    self.start_progress_bar_value + progress_bar_step,
                )
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Преобразование прошло успешно")
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Идет этап сохранения кривой")
            )
            well.save(well_curve=well_curve_to_save, well_id=self.well_id)
            self.signals.progress.emit(
                (
                    self.start_progress_bar_value + progress_bar_step,
                    self.end_progress_bar_value,
                )
            )
            self.signals.message.emit(
                Message(message=self.data_name + "Этап сохранения кривой закончен")
            )
            self.signals.result.emit(None)
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
