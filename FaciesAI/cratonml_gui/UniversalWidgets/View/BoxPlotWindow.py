import numpy as np
from PySide6.QtCharts import (
    QChart,
    QBarSeries,
    QBoxSet,
    QBoxPlotSeries,
    QValueAxis,
    QChartView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGridLayout, QWidget
from pyqtgraph import mkPen

from cratonml_gui.utilities.view_utilities import get_colors


class BoxPlotWindow(QWidget):
    def __init__(self, attributes_data, bins=20, is_light_theme=True):
        super(BoxPlotWindow, self).__init__()
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
        self.boxplot.setPen(mkPen(foreground_color))
        # self.axis_y.setLabelsColor(QColor(foreground_color))

    def plot(self):
        count = len(self.attributes_data)
        box_set = QBoxSet(
            np.min(self.attributes_data),
            np.median(self.attributes_data[: count // 2]),
            np.median(self.attributes_data),
            np.median(self.attributes_data[count // 2 :]),
            np.max(self.attributes_data),
        )
        box_set.append(list(self.attributes_data))
        self.boxplot = QBoxPlotSeries()
        self.boxplot.append(box_set)
        self.chart.addSeries(self.boxplot)
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.boxplot.attachAxis(self.axis_y)

        self.chart.legend().setVisible(False)
        self.chart.createDefaultAxes()
        self._chart_view = QChartView(self.chart)
        self.layout.addWidget(self._chart_view)
        self.setLayout(self.layout)

        self.set_colors(self.is_light_theme)
