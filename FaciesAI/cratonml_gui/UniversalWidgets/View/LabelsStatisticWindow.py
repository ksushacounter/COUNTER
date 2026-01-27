import numpy as np
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QTableWidgetItem, QAbstractItemView, QTableWidget
from pyqtgraph import colormap

from cratonml_gui.UniversalWidgets.View.TableWindow import TableWindow

NUMBER_OF_COLORS = 101


class LabelsStatisticWindow(TableWindow):
    def __init__(self, data_classes):
        super(LabelsStatisticWindow, self).__init__()
        self.data_classes = data_classes

        self.__show_table()

    def __create_table_widget(self):
        """Создает виджет таблицу"""

        classes, counts = np.unique(self.data_classes, return_counts=True)
        all_count = sum(counts)
        vert_headers = []
        self.table_values = np.empty((len(classes), 2))
        for i in range(len(classes)):
            vert_headers.append(str(classes[i]))
            self.table_values[i][0] = counts[i].astype(int)
            self.table_values[i][1] = round(counts[i] / all_count * 100, 2)
        self.hor_headers = ["Количество", "%"]
        ncols = len(self.hor_headers)
        nrows = len(vert_headers)
        self.table_widget = QTableWidget(rowCount=nrows, columnCount=ncols)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setHorizontalHeaderLabels(self.hor_headers)
        self.table_widget.setVerticalHeaderLabels(vert_headers)

    def __show_table(self):
        self.__create_table_widget()
        cmap = colormap.getFromMatplotlib("Blues")
        colors = cmap.getLookupTable(nPts=NUMBER_OF_COLORS)
        font = QFont()
        font.setBold(True)
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                value = self.table_values[row][col]
                item = QTableWidgetItem(str(value))
                item.setFont(font)
                if not np.isnan(value):
                    color = colors[
                        int(self.table_values[row][1] * (NUMBER_OF_COLORS - 1) / 100)
                    ]
                    item.setBackground(QColor(color[0], color[1], color[2]))
                    if sum(color) < 255:
                        item.setForeground(QColor("white"))
                    else:
                        item.setForeground(QColor("black"))
                self.table_widget.setItem(row, col, item)

        self.set_columns_width(self.table_widget, self.hor_headers)

        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)
