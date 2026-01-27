import numpy as np
from PySide6.QtCharts import (
    QChartView,
    QValueAxis,
    QBarCategoryAxis,
    QBarSet,
    QChart,
    QBarSeries,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGridLayout, QWidget

from cratonml_gui.utilities.view_utilities import get_colors


class HistogramWindow(QWidget):
    def __init__(self, attributes_data, bins=20, is_light_theme=True):
        super(HistogramWindow, self).__init__()
        self.attributes_data = attributes_data
        self.bins = bins
        self.is_light_theme = is_light_theme

        self.layout = QGridLayout()
        self.chart = QChart()
        self.bar_series = QBarSeries()
        self.plot()

    def set_colors(self, is_light):
        foreground_color, background_color = get_colors(is_light)
        self.chart.setBackgroundBrush(QColor(background_color))
        self.axis_x.setLabelsColor(QColor(foreground_color))
        self.axis_y.setLabelsColor(QColor(foreground_color))

    def plot(self):
        hist_value = np.empty(self.bins)
        one_bin = (
            np.max(self.attributes_data) - np.min(self.attributes_data)
        ) / self.bins
        sort_attributes_data = sorted(
            self.attributes_data - np.min(self.attributes_data)
        )
        categories = []
        for bin in range(self.bins):
            categories.append(
                str(
                    round((2 * bin + 1) * one_bin / 2 + np.min(self.attributes_data), 2)
                )
            )
            hist_value[bin] = np.where(sort_attributes_data <= (bin + 1) * one_bin)[
                0
            ].shape[0] - sum(hist_value[:bin])
        bar_set = QBarSet("")
        bar_set.append(list(hist_value.astype(int)))
        self.bar_series.append(bar_set)
        self.chart.addSeries(self.bar_series)
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(categories)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.bar_series.attachAxis(self.axis_x)
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(self.axis_y)
        self.bar_series.setBarWidth(1.0)
        self.chart.legend().setVisible(False)

        self._chart_view = QChartView(self.chart)
        self.layout.addWidget(self._chart_view)
        self.setLayout(self.layout)

        self.set_colors(self.is_light_theme)
