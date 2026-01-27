import logging
import os
import platform
import sys
import time
import traceback

from cratonapi import DataConnector
from PySide6 import QtCore
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QSplashScreen,
    QWidget,
    QLabel,
)

from cratonml_gui.Themes.DarkTheme import DarkThemeStylesheet
from cratonml_gui.Themes.LightTheme import LightThemeStylesheet
from cratonml_gui.UniversalControllers.WorkerInfoReader import (
    WorkerGridInfoReader,
    WorkerWellInfoReader,
    WorkerAllStratLevelsInfoReader,
    WorkerCurveDisplayPropertiesReader,
    WorkerCubeInfoReader,
    WorkerOutlineInfoReader,
)
from cratonml_gui.UniversalWidgets.MainWidget.Main import Ui_Main
from cratonml_gui.UniversalWidgets.MainWidget.animated_toggle import AnimatedToggle
from cratonml_gui.templates.WLI.WLI_main import WellLogInterpretation
from cratonml_gui.utilities import Message

current_platform = platform.system()
if current_platform == "Linux":
    from cratonapi.ioconnections import IOSocket
elif current_platform == "Windows":
    from cratonapi.ioconnections import IOPipe

START_PROGRESS_BAR_VALUES = [0, 15, 35, 45, 60, 70, 80, 90, 100]
PROGRESS_BAR_VALUES = [0, 10, 35, 45, 60, 75, 85, 100]
logger = logging.getLogger("__name__")


class MainWindow(QWidget):
    """Класс создает главное окно, читает метаданные и создает виджеты в окне."""

    def __init__(self, splash, progressBar, lineEdit):
        super(MainWindow, self).__init__()
        self.splash = splash
        self.progressBar = progressBar
        self.lineEdit = lineEdit
        self.progressBar.setValue(START_PROGRESS_BAR_VALUES[0])

        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.ui.UpdateBtn.clicked.connect(self.__run_update)

        self.threadpool = QtCore.QThreadPool()

        self.grid_info = {}
        self.cube_info = {}
        self.outline_info = {}
        self.well_info = {}
        self.all_strat_levels_info = {}
        self.curve_tags_info = {}
        self.is_update = False
        self.connection = None
        self.widgets = []
        self.progressBars = []
        self.theme_widget = None
        self.wli_widget = None

        try:
            self.__set_connection()
        except Exception as e:
            self.__create_widgets()
            self.__create_tabs()
            self.__show_all_message(
                Message(
                    message=str(e.args[0])
                    + "\n"
                    + "".join(traceback.format_exception(e)),
                    is_error=True,
                    is_message_for_all=True,
                )
            )
            self.ui.UpdateBtn.setEnabled(True)
        else:
            self.__run_grid_info()
        self.__add_widget()

    def __create_widgets(self):
        self.wli_widget = WellLogInterpretation(
            connection=self.connection,
            well_info=self.well_info,
            all_strat_levels_info=self.all_strat_levels_info,
            curve_tags_info=self.curve_tags_info,
            update_button=self.ui.UpdateBtn,
            threadpool=self.threadpool,
        )
        self.widgets = [
            self.wli_widget
        ]
        for widget in self.widgets:
            widget.settings.widget.ui.progressBar.hide()
        self.progressBars = [
            widget.settings.widget.ui.progressBar for widget in self.widgets
        ]
        for widget in self.widgets:
            widget.set_connection(self.connection)
            if self.theme_widget:
                widget.update_theme(not self.theme_widget.isChecked())

    def __set_connection(self):
        if current_platform == "Linux":
            self.connection = DataConnector(IOSocket(path="/tmp/wseis_launcher_pipe"))
        elif current_platform == "Windows":
            self.connection = DataConnector(
                IOPipe(path=r"\\.\pipe\wseis_launcher_pipe")
            )
        for widget in self.widgets:
            widget.set_connection(self.connection)

    def __add_widget(self):
        self.theme_widget = AnimatedToggle()
        self.theme_widget.setFixedSize(self.theme_widget.sizeHint())
        self.ui.ThemeLayout.addWidget(self.theme_widget)

        self.theme_widget.stateChanged.connect(self.__update_theme)
        self.__update_theme()

    def __update_theme(self):
        if self.theme_widget.isChecked():
            stylesheet = DarkThemeStylesheet().stylesheet
        else:
            stylesheet = LightThemeStylesheet().stylesheet
        self.setStyleSheet(stylesheet)
        for widget in self.widgets:
            widget.update_theme(not self.theme_widget.isChecked())

    def __run_grid_info(self):

        try:
            self.worker_grid_info = WorkerGridInfoReader(
                connection=self.connection,
                start_progress_bar_value=PROGRESS_BAR_VALUES[1],
                end_progress_bar_value=PROGRESS_BAR_VALUES[2],
            )
            self.worker_grid_info.signals.result.connect(self.__run_cube_info)
            self.worker_grid_info.signals.message.connect(self.__show_grid_message)
            self.worker_grid_info.signals.progress.connect(self.__update_progress_bars)
            self.threadpool.start(self.worker_grid_info)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтении метаданных гридов.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __run_cube_info(self, result):
        try:
            self.__get_grid_info(result.info)
            self.worker_cube_info = WorkerCubeInfoReader(
                connection=self.connection,
                start_progress_bar_value=PROGRESS_BAR_VALUES[2],
                end_progress_bar_value=PROGRESS_BAR_VALUES[3],
            )
            self.worker_cube_info.signals.result.connect(self.__run_outline_info)
            self.worker_cube_info.signals.message.connect(self.__show_cube_message)
            self.worker_cube_info.signals.progress.connect(self.__update_progress_bars)
            self.threadpool.start(self.worker_cube_info)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтении метаданных кубов.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __run_outline_info(self, result):
        try:
            self.__get_cube_info(result.info)
            self.worker_outline_info = WorkerOutlineInfoReader(
                connection=self.connection,
                start_progress_bar_value=PROGRESS_BAR_VALUES[3],
                end_progress_bar_value=PROGRESS_BAR_VALUES[4],
            )
            self.worker_outline_info.signals.result.connect(self.__run_well_info)
            self.worker_outline_info.signals.message.connect(
                self.__show_outline_message
            )
            self.threadpool.start(self.worker_outline_info)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтении метаданных контуров.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __run_well_info(self, result):
        try:
            self.__get_outline_info(result.info)
            self.worker_well_info = WorkerWellInfoReader(
                connection=self.connection,
                start_progress_bar_value=PROGRESS_BAR_VALUES[4],
                end_progress_bar_value=PROGRESS_BAR_VALUES[5],
            )
            self.worker_well_info.signals.result.connect(self.__run_curve_tags_info)
            self.worker_well_info.signals.message.connect(self.__show_well_message)
            self.worker_well_info.signals.progress.connect(self.__update_progress_bars)
            self.threadpool.start(self.worker_well_info)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтении метаданных скважин.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __run_curve_tags_info(self, result):
        """Запускает чтение метаданных тэгов кривых."""

        try:
            self.__get_well_info(result)
            self.worker_curve_tags_info = WorkerCurveDisplayPropertiesReader(
                connection=self.connection,
                start_progress_bar_value=PROGRESS_BAR_VALUES[5],
                end_progress_bar_value=PROGRESS_BAR_VALUES[6],
            )
            self.worker_curve_tags_info.signals.result.connect(
                self.__run_strat_levels_info
            )
            self.worker_curve_tags_info.signals.message.connect(
                self.__show_curve_tags_message
            )
            self.worker_curve_tags_info.signals.progress.connect(
                self.__update_progress_bars
            )
            self.threadpool.start(self.worker_curve_tags_info)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтении метаданных тэгов кривых.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __run_strat_levels_info(self, result):
        try:
            self.__get_curve_tags_info(result)
            self.worker_strat_levels_info = WorkerAllStratLevelsInfoReader(
                connection=self.connection,
                start_progress_bar_value=PROGRESS_BAR_VALUES[6],
                end_progress_bar_value=PROGRESS_BAR_VALUES[7],
            )
            self.worker_strat_levels_info.signals.result.connect(
                self.__get_strat_levels_info
            )
            self.worker_strat_levels_info.signals.message.connect(
                self.__show_strat_level_message
            )
            self.worker_strat_levels_info.signals.progress.connect(
                self.__update_progress_bars
            )
            self.threadpool.start(self.worker_strat_levels_info)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтении метаданных стратиграфических уровней.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __update_progress_bars(self, progress_bar_values, progress_bars=None):
        """
        Изменяет индикаторы прогресса self.progressBars/progress_bars в пределе значений [current_value + 1, value_end]
        с интервалом 0.01 секунда.
        """

        try:
            for i in range(progress_bar_values[0] + 1, progress_bar_values[1] + 1):
                time.sleep(0.01)
                if progress_bars is None:
                    for pb in self.progressBars:
                        pb.setValue(i)
                else:
                    for pb in progress_bars:
                        pb.setValue(i)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении индикаторов прогресса в виджетах.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __get_grid_info(self, info):
        """Обновляет метаданные гридов."""

        try:
            self.grid_info = info
            if self.splash.isVisible():
                self.__update_progress_bars(
                    progress_bar_values=(
                        self.progressBar.value(),
                        START_PROGRESS_BAR_VALUES[2],
                    ),
                    progress_bars=[self.progressBar],
                )
            # if not self.grid_info and len(self.progressBars) > 0:
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных гридов.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __get_cube_info(self, info):
        """Обновляет метаданные кубов."""

        try:
            self.cube_info = info
            if self.splash.isVisible():
                self.__update_progress_bars(
                    progress_bar_values=(
                        self.progressBar.value(),
                        START_PROGRESS_BAR_VALUES[3],
                    ),
                    progress_bars=[self.progressBar],
                )
            # if not self.cube_info and len(self.progressBars) > 0:
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных кубов.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __get_outline_info(self, info):
        """Обновляет метаданные контуров."""

        try:
            self.outline_info = info
            if self.splash.isVisible():
                self.__update_progress_bars(
                    progress_bar_values=(
                        self.progressBar.value(),
                        START_PROGRESS_BAR_VALUES[4],
                    ),
                    progress_bars=[self.progressBar],
                )
            # if not self.outline_info and len(self.progressBars) > 0:
            #     if self.ssfa_widget.settings.widget.ui.progressBar in self.progressBars:
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных контуров.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __get_well_info(self, result):
        """Обновляет метаданные скважин."""

        try:
            self.well_info = result.info
            if self.splash.isVisible():
                self.__update_progress_bars(
                    progress_bar_values=(
                        self.progressBar.value(),
                        START_PROGRESS_BAR_VALUES[5],
                    ),
                    progress_bars=[self.progressBar],
                )
            if not self.well_info and len(self.progressBars) > 0:
                self.progressBars.remove(self.wli_widget.settings.widget.ui.progressBar)
                # if self.ssfa_widget.settings.widget.ui.progressBar in self.progressBars:
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных скважин.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __get_curve_tags_info(self, result):
        """Обновляет метаданные тэгов кривых."""

        try:
            self.curve_tags_info = result.info
            if self.splash.isVisible():
                self.__update_progress_bars(
                    progress_bar_values=(
                        self.progressBar.value(),
                        START_PROGRESS_BAR_VALUES[6],
                    ),
                    progress_bars=[self.progressBar],
                )
            if not self.curve_tags_info and len(self.progressBars) > 0:
                if self.wli_widget.settings.widget.ui.progressBar in self.progressBars:
                    self.progressBars.remove(
                        self.wli_widget.settings.widget.ui.progressBar
                    )
                # if self.ssfa_widget.settings.widget.ui.progressBar in self.progressBars:
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных тэгов кривых.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __get_strat_levels_info(self, result):
        """
        Обновляет метаданные стратиграфических уровней.
        Если флаг self.is_update = True, обновляет данные в виджете. Иначе создает виджет.
        """

        try:
            self.all_strat_levels_info = result.info
            if self.all_strat_levels_info is None and len(self.progressBars) > 0:
                if self.wli_widget.settings.widget.ui.progressBar in self.progressBars:
                    self.progressBars.remove(
                        self.wli_widget.settings.widget.ui.progressBar
                    )
                # if self.ssfa_widget.settings.widget.ui.progressBar in self.progressBars:

            if self.splash.isVisible():
                self.__update_progress_bars(
                    progress_bar_values=(
                        self.progressBar.value(),
                        START_PROGRESS_BAR_VALUES[7],
                    ),
                    progress_bars=[self.progressBar],
                )
            if self.is_update:
                self.__update()
            else:
                self.__create_widgets()
                self.__create_tabs()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных стратиграфических уровней.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __create_tabs(self):
        try:
            self.ui.MainTabWidget.addTab(self.wli_widget, "Интерпретация данных ГИС")
            if self.splash.isVisible():
                self.__update_progress_bars(
                    progress_bar_values=(
                        self.progressBar.value(),
                        START_PROGRESS_BAR_VALUES[8],
                    ),
                    progress_bars=[self.progressBar],
                )
            self.show()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении виджетов.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __run_update(self, signal):
        """
        Запускает обновление.
        Создает новое соединение с WSeis. Запускает чтение метаданных.
        """

        try:
            self.__clear_widgets()
            self.__show_all_message(
                Message(
                    message=f"Идет этап обновления данных", is_message_for_all=True
                ),
                set_line_count_zero=True,
            )
            self.progressBars = [
                widget.settings.widget.ui.progressBar for widget in self.widgets
            ]
            self.__update_progress_bars(
                progress_bar_values=(PROGRESS_BAR_VALUES[0], PROGRESS_BAR_VALUES[1])
            )
            self.is_update = True
            if self.connection:
                self.connection.connection.disconnect()

                self.connection = None
            try:
                self.__set_connection()
            except Exception as e:
                self.__show_all_message(
                    Message(
                        message=str(e.args[0])
                        + "\n"
                        + "".join(traceback.format_exception(e)),
                        is_error=True,
                        is_message_for_all=True,
                    )
                )
                self.is_update = False
                for widget in self.widgets:
                    # widget.settings.widget.ui.progressBar.hide()
                    widget.settings.widget.stop_gif()
                self.ui.UpdateBtn.setEnabled(True)
            else:
                self.__run_grid_info()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении данных.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __clear_widgets(self):
        """Делает виджет не активным. Показывает индикатор прогресса. Отчищает окно состояния."""

        try:
            for widget in self.widgets:
                widget.set_enabled(False)
                widget.ui.MessageLineEdit.clear()
                widget.message_widget.ui.MessageTextEdit.clear()
                widget.settings.widget.ui.progressBar.setValue(0)
                # widget.settings.widget.ui.progressBar.show()
                widget.settings.widget.add_gif()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при отчистке главного виджета.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __update(self):
        """
        Вызывает функцию обновления виджета. Делает кнопку обновления активной.
        Если обновление прошла успешно(все метаданные не None), то делает виджет активным
        """

        try:
            self.__update_widgets()
            self.is_update = False
            self.__show_all_message(
                Message(
                    message=f"Этап обновления данных закончен", is_message_for_all=True
                )
            )

            for widget in self.widgets:
                widget.set_enabled(True)
            self.ui.UpdateBtn.setEnabled(True)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении виджетов.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __update_widgets(self):
        """Вызывает функцию обновления метаданных виджета."""

        try:
            self.wli_widget.settings.update_info(
                well_info=self.well_info,
                curve_tags_info=self.curve_tags_info,
                all_strat_levels_info=self.all_strat_levels_info,
            )
            self.wli_widget.view.update_info(
                well_info=self.well_info, curve_tags_info=self.curve_tags_info
            )
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных в виджетах.",
                is_warning=True,
                is_message_for_all=True,
            )
            self.__show_all_message(message)
            logger.error(e, exc_info=True)

    def __show_all_message(self, result, set_line_count_zero=False):
        """Выводит сообщение предназначенное для всех виджетов в окно состояния и записывает его в логи."""

        try:
            if result.is_error:
                logger.error(result.message)
            elif result.is_warning:
                logger.warning(result.message)
            else:
                logger.info(result.message)
            for widget in self.widgets:
                widget.show_message(result, set_line_count_zero)
            if self.splash.isVisible():
                message = result.message
                if result.is_error:
                    message = message.split("\n")[0]
                self.lineEdit.setText(message)
        except Exception as e:
            logger.error(e, exc_info=True)

    def __show_message(self, result, widgets):
        if result.is_error:
            logger.error(result.message)
            for widget in widgets:
                widget.set_enabled(False)
            self.ui.UpdateBtn.setEnabled(True)
        elif result.is_warning:
            logger.warning(result.message)
            for widget in widgets:
                widget.set_enabled(False)
            self.ui.UpdateBtn.setEnabled(True)
        else:
            logger.info(result.message)
        for widget in widgets:
            widget.show_message(result)
        if self.splash.isVisible():
            message = result.message
            if result.is_error:
                message = message.split("\n")[0]
            self.lineEdit.setText(message)

    def __show_grid_message(self, result):
        try:
            self.__show_message(result, [])
        except Exception as e:
            logger.error(e, exc_info=True)

    def __show_cube_message(self, result):
        try:
            self.__show_message(result, [])
        except Exception as e:
            logger.error(e, exc_info=True)

    def __show_outline_message(self, result):
        try:
            self.__show_message(result, [])
        except Exception as e:
            logger.error(e, exc_info=True)

    def __show_well_message(self, result):
        try:
            if self.widgets:
                self.__show_message(result, [self.wli_widget])
            else:
                self.__show_message(result, [])
        except Exception as e:
            logger.error(e, exc_info=True)

    def __show_curve_tags_message(self, result):
        try:
            if self.widgets:
                self.__show_message(result, [self.wli_widget])
            else:
                self.__show_message(result, [])
        except Exception as e:
            logger.error(e, exc_info=True)

    def __show_strat_level_message(self, result):
        try:
            if self.widgets:
                self.__show_message(result, [self.wli_widget])
            else:
                self.__show_message(result, [])
        except Exception as e:
            logger.error(e, exc_info=True)

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setButtonText(QMessageBox.Yes, " Да ")
        msg_box.setButtonText(QMessageBox.No, " Нет ")
        msg_box.setText("Вы уверены, что хотите закрыть приложение?")
        msg_box.setWindowTitle("Подтверждение")
        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            for widget in self.widgets:
                widget.close_widgets()

            if self.connection:
                self.connection.connection.disconnect()
            event.accept()
        else:
            event.ignore()

    def showEvent(self, event):
        self.splash.finish(self)
        event.accept()


def main():
    app = QApplication(sys.argv)
    log_path = os.getenv("LOCALAPPDATA") + "/StratoScope/MLToolBox/Logs"
    os.makedirs(log_path, exist_ok=True)
    logging.basicConfig(
        filename=log_path + "/mltoolbox.log",
        format="%(asctime)s %(levelname)s %(message)s",
        filemode="w",
    )
    logger.setLevel(logging.DEBUG)

    splash_path = "./cratonml_gui/icons/splash.png"
    if getattr(sys, "frozen", False):
        splash_path = os.path.join(sys._MEIPASS, splash_path)
    pixmap = QPixmap(splash_path)
    splash = QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)
    splash.setEnabled(False)

    gif_path = "./cratonml_gui/Themes/gifs/loading_20x20.gif"
    if getattr(sys, "frozen", False):
        gif_path = os.path.join(sys._MEIPASS, gif_path)
    movie = QMovie(gif_path)
    gif_label = QLabel(splash)
    gif_label.setGeometry(880, 620, 20, 20)
    gif_label.setMovie(movie)
    movie.start()

    progressBar = QProgressBar(splash)
    progressBar.setGeometry(400, 620, 460, 20)
    progressBar.setStyleSheet(
        """QProgressBar {
                                  color: #000000;
                                  font-weight: 700;
                                  border: 1px solid #333399;
                                  border-radius: 4px;
                                  text-align: center;
                                }
                                QProgressBar:chunk {
                                  background-color: #333399;
                                }"""
    )
    lineEdit = QLineEdit(splash)
    lineEdit.setReadOnly(True)
    lineEdit.setGeometry(400, 580, 500, 30)
    lineEdit.setStyleSheet(
        """QLineEdit {
                                color: #999999;
                                font-weight: 600;
                                border: 1px solid #fff;
                              }"""
    )
    splash.show()
    app.processEvents()

    window = MainWindow(splash, progressBar, lineEdit)

    return app.exec_()


if getattr(sys, "frozen", False):
    main()
