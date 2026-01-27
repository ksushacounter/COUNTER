from abc import abstractmethod

from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QWidget, QGridLayout


class TableWindow(QWidget):
    """Класс для создания таблицы."""

    def __init__(
        self,
    ):
        super(TableWindow, self).__init__()
        self.layout = QGridLayout()

    @abstractmethod
    def __create_table_widget(self):
        """Создает виджет таблицу"""

        pass

    @abstractmethod
    def __show_table(self):
        """Заполняет таблицу и её заголовки."""

        pass

    @staticmethod
    def set_columns_width(table_widget, columns):
        """Устанавливает ширину колонки таблицы в максимальную ширину из заголовка и всех элементов столбца"""

        font_metrics = QFontMetrics(table_widget.font())
        for col in range(table_widget.columnCount()):
            header_text = columns[col]
            header_width = font_metrics.horizontalAdvance(header_text)
            max_content_width = 0
            for row in range(table_widget.rowCount()):
                cell_text = table_widget.item(row, col).text()
                max_content_width = max(
                    max_content_width, font_metrics.horizontalAdvance(cell_text)
                )
            table_widget.setColumnWidth(col, max(header_width, max_content_width) + 30)
