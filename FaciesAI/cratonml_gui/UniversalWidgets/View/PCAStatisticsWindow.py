from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QTableWidget,
    QAbstractItemView,
    QTableWidgetItem,
)

from cratonml_gui.UniversalWidgets.View.TableWindow import TableWindow

NCOLS = 3
NUMBER_OF_COLORS = 201


class PCAStatisticsWindow(TableWindow):
    def __init__(
        self, singular_values, explained_variance_ratio, sum_explained_variance_ratio
    ):
        super(PCAStatisticsWindow, self).__init__()
        self.singular_values = singular_values
        self.explained_variance_ratio = explained_variance_ratio
        self.sum_explained_variance_ratio = sum_explained_variance_ratio

        self.__show_table()

    def __create_table_widget(self):
        """Создает виджет таблицу"""

        ncols = NCOLS
        nrows = len(self.singular_values)
        vert_headers = [str(i) for i in range(1, ncols + 1)]
        self.hor_headers = [
            "Eigenvalue",
            "Percentage of Variance",
            "Cumulative",
        ]
        self.table_widget = QTableWidget(rowCount=nrows, columnCount=ncols)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setHorizontalHeaderLabels(self.hor_headers)
        self.table_widget.setVerticalHeaderLabels(vert_headers)

    def __show_table(self):
        """Заполняет таблицу и её заголовки."""

        # cmap = colormap.getFromMatplotlib("RdYlGn")
        # colors = cmap.getLookupTable(nPts=NUMBER_OF_COLORS)

        self.__create_table_widget()

        font = QFont()
        font.setBold(True)
        for j in range(len(self.singular_values)):
            value = round(self.singular_values[j], 4)
            item = QTableWidgetItem(str(value))
            # if not np.isnan(value):
            #     color = colors[
            #         NUMBER_OF_COLORS // 2
            #         + int(value * NUMBER_OF_COLORS // 2)
            #         - (NUMBER_OF_COLORS + 1) % 2
            #     ]
            #     item.setBackground(QColor(color[0], color[1], color[2]))
            #     item.setForeground(QColor("black"))
            item.setFont(font)
            self.table_widget.setItem(j, 0, item)

            value = round(self.explained_variance_ratio[j] * 100, 2)
            item = QTableWidgetItem(str(value) + "%")
            item.setFont(font)
            self.table_widget.setItem(j, 1, item)

            value = round(self.sum_explained_variance_ratio[j] * 100, 2)
            item = QTableWidgetItem(str(value) + "%")
            item.setFont(font)
            self.table_widget.setItem(j, 2, item)
        self.set_columns_width(self.table_widget, self.hor_headers)
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)
