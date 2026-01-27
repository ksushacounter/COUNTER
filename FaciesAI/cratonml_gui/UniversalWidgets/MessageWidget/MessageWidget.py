from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget

from cratonml_gui.Themes.DarkTheme import DarkThemeStylesheet
from cratonml_gui.Themes.LightTheme import LightThemeStylesheet
from cratonml_gui.UniversalWidgets.MessageWidget.MessageWidget_ui import (
    Ui_MessageWidget,
)


class MessageWidget(QWidget):
    def __init__(
        self,
    ):
        super(MessageWidget, self).__init__()

        self.ui = Ui_MessageWidget()
        self.ui.setupUi(self)

    def update_style_sheet(self, is_light_theme):
        if is_light_theme:
            stylesheet = LightThemeStylesheet().stylesheet
        else:
            stylesheet = DarkThemeStylesheet().stylesheet

        self.setStyleSheet(stylesheet)

    def open_message_widget(self, text, is_light_theme=True):
        """Записывает текст, переносит курсор в конец и открывает окно сообщений."""

        self.update_style_sheet(is_light_theme)
        self.ui.MessageTextEdit.setHtml(text)
        self.ui.MessageTextEdit.moveCursor(QTextCursor.End)
        self.show()

    def insert_html(self, html_message):
        """Вставляет строчку в журнал событий."""

        self.ui.MessageTextEdit.append("")
        self.ui.MessageTextEdit.insertHtml(html_message)
