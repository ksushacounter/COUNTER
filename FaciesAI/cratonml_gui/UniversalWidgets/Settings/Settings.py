import logging
import time
from abc import abstractmethod

from cratonml_gui.utilities import Message

logger = logging.getLogger("__name__")


class Settings:
    def __init__(
        self,
        connection,
        threadpool,
        show_message_func,
        signal_for_visualization_result,
        set_enabled_func,
    ):
        super(Settings, self).__init__()
        self.connection = connection
        self.threadpool = threadpool
        self.show_message_func = show_message_func
        self.signal_for_visualization_result = signal_for_visualization_result
        self.set_enabled_func = set_enabled_func

        self.widget = None
        self.caching = None

    @abstractmethod
    def collecting_data_from_widget(self):
        """Запускает парсинг данных с виджета."""

        pass

    def set_enabled(self, state):
        """Если state=True делает элементы активными. Иначе делает их не активными."""

        self.widget.ui.SettingsFrame.setEnabled(state)
        self.widget.stop_gif()
        # self.widget.ui.progressBar.hide()

    def update_progress_bar(self, progress_bar_values):
        """Обновляет прогресс бар."""

        try:
            for i in range(
                int(progress_bar_values[0]) + 1, int(progress_bar_values[1]) + 1
            ):
                time.sleep(0.01)
                self.widget.ui.progressBar.setValue(i)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении индикатора выполнения.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def set_connection(self, connection):
        """Устанавливает новое соединение с WSeis."""

        self.connection = connection
        if self.caching is not None:
            self.caching.set_is_connection_update(True)

    def update_info(
        self,
        well_info=None,
        grid_info=None,
        cube_info=None,
        all_strat_levels_info=None,
        curve_tags_info=None,
        outline_info=None,
    ):
        """Обновляет метаданные в виджете."""

        try:
            if well_info is not None:
                self.well_info = well_info
            if grid_info is not None:
                self.grid_info = grid_info
            if cube_info is not None:
                self.cube_info = cube_info
            if all_strat_levels_info is not None:
                self.all_strat_levels_info = all_strat_levels_info
            if curve_tags_info is not None:
                self.curve_tags_info = curve_tags_info
            if outline_info is not None:
                self.outline_info = outline_info

            self.widget.update_info(
                well_info=well_info,
                grid_info=grid_info,
                cube_info=cube_info,
                all_strat_levels_info=all_strat_levels_info,
                curve_tags_info=curve_tags_info,
                outline_info=outline_info,
            )
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных в виджете.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    @abstractmethod
    def prepare_data(self, result, ind=None):
        """Подготавливает данные для визуализации."""

        pass

    def emit_signal(self, result, ind=None):
        """Вызывает сигнал для визуализации."""

        try:
            self.caching.set_is_connection_update(False)
            self.signal_for_visualization_result.emit(self.prepare_data(result, ind))
        except Exception as e:
            message = Message(
                message="Произошла ошибка при вызове сигнала для визуализации.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)
