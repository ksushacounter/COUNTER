import numpy as np
from PySide6.QtCharts import QChart, QPieSeries, QChartView
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGridLayout, QWidget
from pyqtgraph import colormap

from cratonml_gui.utilities.view_utilities import get_colors


class PieChartWindow(QWidget):
    def __init__(
        self, data_classes, uniq_labels=None, cmap="turbo", is_light_theme=True
    ):
        super(PieChartWindow, self).__init__()
        self.data_classes = data_classes
        self.uniq_labels = uniq_labels
        self.cmap = cmap
        self.is_light_theme = is_light_theme

        self.layout = QGridLayout()
        self.chart = QChart()
        self.plot()

    def set_colors(self, is_light):
        foreground_color, background_color = get_colors(is_light)
        self.chart.setBackgroundBrush(QColor(background_color))
        for slice in self.slices:
            slice.setLabelColor(QColor(foreground_color))

    def plot(self):
        pie_chart = QPieSeries()
        classes, counts = np.unique(self.data_classes, return_counts=True)
        cmap = colormap.get(self.cmap)
        if self.uniq_labels is not None:
            colors = cmap.getLookupTable(nPts=len(self.uniq_labels))
        self.slices = []
        for i in range(len(classes)):
            self.slices.append(pie_chart.append(str(classes[i]), counts[i]))
            if self.uniq_labels is not None:
                color = colors[np.where(self.uniq_labels == classes[i])[0][0]]
                self.slices[i].setBrush(QColor(color[0], color[1], color[2]))
        self.chart.legend().hide()
        pie_chart.setLabelsVisible()
        self.chart.addSeries(pie_chart)
        self._chart_view = QChartView(self.chart)
        self.layout.addWidget(self._chart_view)
        self.setLayout(self.layout)

        self.set_colors(self.is_light_theme)
