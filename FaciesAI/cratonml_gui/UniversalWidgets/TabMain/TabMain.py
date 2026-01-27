import logging

from PySide6.QtWidgets import QWidget

from cratonml_gui.UniversalWidgets.MessageWidget.MessageWidget import MessageWidget
from cratonml_gui.UniversalWidgets.TabMain.TabMain_ui import Ui_TabMainWidget
from cratonml_gui.utilities import Message
from cratonml_gui.utilities.Signals import WidgetSignals

logger = logging.getLogger("__name__")


class TabMain(QWidget):
    def __init__(self, update_button, threadpool):
        super(TabMain, self).__init__()
        self.update_button = update_button
        self.threadpool = threadpool

        self.ui = Ui_TabMainWidget()
        self.ui.setupUi(self)
        self.message_widget = MessageWidget()
        self.signals = WidgetSignals()
        self.signal_for_visualization_result = (
            self.signals.signal_for_visualization_result
        )

        self.settings = None
        self.view = None
        self.message_line_count = 0
        self.is_light_theme = True

        self.__create_callbacks()

    def __create_callbacks(self):
        """Задает реакции на нажатие кнопок"""

        try:
            self.ui.OpenMessageWidgetBtn.clicked.connect(self.__open_message_widget)
            self.ui.InputDataHideBtn.clicked.connect(self.__hide_input_data_widget)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при установке реакций на действия пользователя в главном окне.",
                is_warning=True,
            )
            self.show_message(message)
            self.set_enabled(True)
            logger.error(e, exc_info=True)

    def __hide_input_data_widget(self):
        """Показывает или убирает блок входных данных."""

        try:
            if self.ui.SettingsFrame.isVisible():
                self.ui.SettingsFrame.hide()
            else:
                self.ui.SettingsFrame.show()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при показе/скрытии блока входных данных.",
                is_warning=True,
            )
            self.show_message(message)
            self.set_enabled(True)
            logger.error(e, exc_info=True)

    def __open_message_widget(self):
        """Открывает окно сообщений."""

        try:
            text = self.message_widget.ui.MessageTextEdit.toHtml()
            self.message_widget = MessageWidget()
            self.message_widget.open_message_widget(
                text=text, is_light_theme=self.is_light_theme
            )
        except Exception as e:
            message = Message(
                message="Произошла ошибка при открытии окна сообщений.", is_warning=True
            )
            self.show_message(message)
            self.set_enabled(True)
            logger.error(e, exc_info=True)

    def set_enabled(self, state):
        """Если state=True делает элементы активными. Иначе делает их не активными."""

        try:
            self.settings.set_enabled(state)
            self.view.set_enabled(state)
            self.update_button.setEnabled(state)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при разблокировке/блокировке интерфейса.",
                is_warning=True,
            )
            self.show_message(message)
            logger.error(e, exc_info=True)

    def set_connection(self, connection):
        """Устанавливает новое соединение с WSeis."""

        try:
            self.settings.set_connection(connection)
            self.view.set_connection(connection)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при установке нового соединения с WSeis.",
                is_warning=True,
            )
            self.show_message(message)
            self.set_enabled(True)
            logger.error(e, exc_info=True)

    def show_message(self, result, set_line_count_zero=False):
        """Выводит сообщения в окно состояния и записывает в логи."""

        try:
            if set_line_count_zero:
                self.message_line_count = 0
            self.message_line_count += 1
            message = str(self.message_line_count) + ". "
            message += result.message

            if result.is_error:
                if not result.is_message_for_all:
                    logger.error(message)
                message = message.split("\n")[0]
                html_message = '<span style=" color:#ff0000;">{}</span>'.format(message)
                self.ui.MessageLineEdit.setStyleSheet("color: #ff0000;")
            elif result.is_warning:
                if not result.is_message_for_all:
                    logger.warning(message)
                html_message = '<span style=" color:#ff0000;">{}</span>'.format(message)
                self.ui.MessageLineEdit.setStyleSheet("color: #ff0000;")
            else:
                if not result.is_message_for_all:
                    logger.info(message)
                html_message = '<span style=" color:#2eb50d;">{}</span>'.format(message)
                self.ui.MessageLineEdit.setStyleSheet("color: #2eb50d;")
            self.ui.MessageLineEdit.setText(message)
            self.message_widget.insert_html(html_message)
        except Exception as e:
            logger.error(e, exc_info=True)

    def close_widgets(self):
        """Закрывает все виджеты."""

        try:
            self.settings.widget.close_widgets()
            # self.view.widget.close_widgets()
            self.message_widget.close()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при закрытии всех дополнительных окон.",
                is_warning=True,
            )
            self.show_message(message)
            self.set_enabled(True)
            logger.error(e, exc_info=True)

    def update_theme(self, is_light_theme):
        self.is_light_theme = is_light_theme
        self.settings.widget.update_theme(is_light_theme)
        self.view.update_theme(is_light_theme)
        self.message_widget.update_style_sheet(is_light_theme)
