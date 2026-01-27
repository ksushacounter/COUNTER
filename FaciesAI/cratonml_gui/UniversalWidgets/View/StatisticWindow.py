import numpy as np
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QTabWidget,
    QTableWidget,
    QAbstractItemView,
    QTableWidgetItem,
)
from pyqtgraph import colormap

from cratonml_gui.UniversalWidgets.View.TableWindow import TableWindow

NUMBER_OF_COLORS = 201


class StatisticWindow(TableWindow):
    def __init__(self, matrix_list):
        super(StatisticWindow, self).__init__()
        self.matrix_list = matrix_list

        self.tab = QTabWidget()
        self.__show_table()

    def __create_table_widget(self):
        """Создает виджет таблицу"""

        ncols = self.matrix.shape[0]
        nrows = ncols
        labels = ["Класс: {i}".format(i=i) for i in range(ncols)]
        self.table_widget = QTableWidget(rowCount=nrows, columnCount=ncols)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setHorizontalHeaderLabels(labels)
        self.table_widget.setVerticalHeaderLabels(labels)

    def __show_table(self):
        """Заполняет таблицу и её заголовки."""

        cmap = colormap.getFromMatplotlib("RdYlGn")
        colors = cmap.getLookupTable(nPts=NUMBER_OF_COLORS)
        titles = [
            "Pearson correlation coefficient",
            "Spearman correlation coefficient",
            "Pearson correlation p-value",
            "Spearman correlation p-value",
        ]
        for i in range(len(titles)):
            self.matrix = self.matrix_list[i]

            self.__create_table_widget()

            font = QFont()
            font.setBold(True)
            for k in range(self.matrix.shape[0]):
                for j in range(self.matrix.shape[1]):
                    value = round(self.matrix[k][j], 2)
                    item = QTableWidgetItem(str(value))
                    if not np.isnan(value):
                        color = colors[
                            NUMBER_OF_COLORS // 2
                            + int(value * NUMBER_OF_COLORS // 2)
                            - (NUMBER_OF_COLORS + 1) % 2
                        ]
                        item.setBackground(QColor(color[0], color[1], color[2]))
                        item.setForeground(QColor("black"))
                    item.setFont(font)
                    self.table_widget.setItem(k, j, item)
            self.tab.insertTab(i, self.table_widget, titles[i])
        self.tab.setCurrentIndex(0)
        self.layout.addWidget(self.tab)
        self.setLayout(self.layout)
