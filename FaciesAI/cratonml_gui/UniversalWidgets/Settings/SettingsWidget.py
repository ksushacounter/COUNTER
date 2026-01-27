import os
import sys
from abc import abstractmethod

from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QWidget, QLabel


class SettingsWidget(QWidget):
    def __init__(self):
        super(SettingsWidget, self).__init__()
        self.is_light_theme = True
        self.ui = None
        self.gif = None
        self.worker_gif = None

    @abstractmethod
    def __create_callbacks(self):
        """Задает реакции на нажатие кнопок."""

        pass

    @abstractmethod
    def update_data(self, data):
        """Запускает обновление всех данных, на данные в конфигурационном файле (*.ini)."""

        pass

    @abstractmethod
    def update_data_widgets(self):
        """Обновляет данные в виджетах."""

        pass

    @abstractmethod
    def create_config_parser(self):
        """Создает парсер конфигурационного файла."""

        pass

    def update_config_data(self):
        """Загружает данные из конфигурационного файла (*.ini) и обновляет их в виджете."""

        self.config_parser = self.create_config_parser()
        data = self.config_parser.upload_config()
        self.update_data(data)
        self.config_parser.create_callbacks()
        self.config_parser.prepare_config()
        # self.ui.progressBar.hide()

    def update_info(
        self,
        well_info,
        grid_info,
        cube_info,
        all_strat_levels_info,
        curve_tags_info,
        outline_info,
    ):
        """
        Обновляет метаданные. Обновляет все элементы виджета связанные с метаданными.
        Загружает данные из конфигурационного файла (*.ini) и обновляет их в виджете.
        """

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
        self.config_parser = None

        self.update_data_widgets()
        self.update_config_data()

    @abstractmethod
    def close_widgets(self):
        """Закрывает все виджеты."""

        pass

    @abstractmethod
    def update_theme(self, is_light_theme):

        pass

    def add_gif(self):
        if self.is_light_theme:
            gif_path = "./cratonml_gui/Themes/gifs/light/loading_24x24.gif"
        else:
            gif_path = "./cratonml_gui/Themes/gifs/dark/loading_24x24.gif"
        if getattr(sys, "frozen", False):
            gif_path = os.path.join(sys._MEIPASS, gif_path)
        if self.gif is None:
            self.gif = QMovie(gif_path)
            # self.gif_label = QLabel("")
            # self.gif_label.setMovie(self.gif)
            # self.ui.progressLayout.addWidget(self.gif_label)
            self.ui.gifLabel.setMovie(self.gif)
            self.gif.jumpToFrame(0)
        self.ui.progressFrame.show()
        self.gif.start()

    def stop_gif(self):
        if self.gif is not None:
            self.gif.stop()
            # self.ui.progressLayout.removeWidget(self.gif_label)
            # self.gif_label.deleteLater()
            # self.gif_label.clear()
            self.ui.gifLabel.clear()
            self.ui.progressFrame.hide()
            self.gif = None
            # self.gif_label = None
