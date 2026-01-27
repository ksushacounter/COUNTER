from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QWidget
from pyqtgraph import AxisItem, mkPen, PlotWidget

from cratonml_gui.utilities.view_utilities import get_colors

FONT_SIZE = 11


class CurveWindow(QWidget):
    def __init__(
        self,
        x,
        y,
        title=None,
        x_label=None,
        y_label=None,
        vertical_line=None,
        is_light_theme=True,
    ):
        super(CurveWindow, self).__init__()
        self.x = x
        self.y = y
        self.x_label = x_label
        self.y_label = y_label
        self.vertical_line = vertical_line
        self.title = title
        self.is_light_theme = is_light_theme

        self.font = QFont()
        self.font.setPointSize(FONT_SIZE)

        self.layout = QHBoxLayout()
        self.plot()

    def set_colors(self, is_light):
        foreground_color, background_color = get_colors(is_light)
        self.widget.setBackground(None)

        left = self.widget.getAxis("left")
        left.setPen(foreground_color)
        left.setTextPen(foreground_color)
        bottom = self.widget.getAxis("bottom")
        bottom.setPen(foreground_color)
        bottom.setTextPen(foreground_color)
        right = self.widget.getAxis("right")
        right.setPen(foreground_color)
        right.setTextPen(background_color)
        self.widget.getAxis("top").setPen(foreground_color)

        if self.x_label is not None:
            bottom.label.setDefaultTextColor(foreground_color)
        if self.y_label is not None:
            left.label.setDefaultTextColor(foreground_color)
        if self.title is not None:
            self.widget.setTitle(self.title, color=foreground_color, size="13pt")
        if self.vertical_line is not None:
            self.legend.setLabelTextColor(foreground_color)
            self.legend.setBrush(background_color)
            self.legend.clear()
            self.line.setPen(mkPen(color=foreground_color, width=2, style=Qt.DashLine))
            self.line.opts = {
                "pen": mkPen(color=foreground_color, width=2, style=Qt.DashLine)
            }
            self.legend.addItem(self.line, name="Оптимальное количество кластеров")

    def plot(self):
        self.widget = PlotWidget()
        self.widget.plot(self.x, self.y, pen=mkPen(color="darkCyan", width=2))
        self.widget.setMouseEnabled(False, False)

        axis_left = AxisItem(orientation="left")
        axis_left.setTickFont(self.font)
        axis_bottom = AxisItem(orientation="bottom")
        axis_bottom.setTickFont(self.font)
        axis_right = AxisItem(orientation="right", tickPen=mkPen(width=1e-10))
        axis_top = AxisItem(
            orientation="top", tickPen=mkPen(width=1e-10), showValues=False
        )
        self.widget.setAxisItems(
            {
                "left": axis_left,
                "bottom": axis_bottom,
                "right": axis_right,
                "top": axis_top,
            }
        )
        if self.x_label is not None:
            self.widget.setLabel(
                axis="bottom", text=self.x_label, **{"font-size": "13pt"}
            )
        if self.y_label is not None:
            self.widget.setLabel(
                axis="left", text=self.y_label, **{"font-size": "13pt"}
            )

        self.legend = self.widget.addLegend(
            labelTextColor="black", labelTextSize="11pt", pen="gray", offset=(0, 1)
        )
        self.line = self.widget.addLine(
            pos=self.vertical_line,
            angle=90,
            pen=mkPen(color="black", width=2, style=Qt.DashLine),
        )
        self.set_colors(self.is_light_theme)

        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)
