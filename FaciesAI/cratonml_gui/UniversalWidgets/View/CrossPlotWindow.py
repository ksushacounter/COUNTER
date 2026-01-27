import numpy as np
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget
from pyqtgraph import AxisItem, PlotWidget, mkPen, ScatterPlotItem, mkBrush, TextItem

from cratonml_gui.utilities.view_utilities import get_colors

FONT_SIZE = 11


class CrossPlotWindow(QWidget):
    """Класс для создания кросс-плота."""

    def __init__(self, is_light_theme):
        super(CrossPlotWindow, self).__init__()

        self.is_light_theme = is_light_theme
        self.plot_widget = None
        self.scatter = None
        self.title = ""
        self.text_items = []
        self.text_parent = None

        self.create_plot_widget()

    def create_plot_widget(self):
        """Создает виджет для визуализации."""

        font = QFont()
        font.setPointSize(FONT_SIZE)

        axis_left = AxisItem(orientation="left")
        axis_left.setTickFont(font)
        axis_bottom = AxisItem(orientation="bottom")
        axis_bottom.setTickFont(font)
        axis_right = AxisItem(orientation="right", tickPen=mkPen(width=1e-10))
        axis_top = AxisItem(
            orientation="top", tickPen=mkPen(width=1e-10), showValues=False
        )
        self.plot_widget = PlotWidget()
        self.plot_widget.setAxisItems(
            {
                "left": axis_left,
                "bottom": axis_bottom,
                "right": axis_right,
                "top": axis_top,
            }
        )

        self.scatter = ScatterPlotItem(size=10, brush=mkBrush(30, 255, 35, 255))
        self.legend = self.plot_widget.addLegend(
            labelTextColor="black", labelTextSize="11pt", offset=(1, 1), brush="white"
        )

    def set_colors(self, is_light):
        """Устанавливает цвета фона, осей и заголовков."""

        foreground_color, background_color = get_colors(is_light)
        self.plot_widget.setBackground(None)
        self.plot_widget.setTitle(self.title, color=foreground_color, size="13pt")

        left = self.plot_widget.getAxis("left")
        left.setPen(foreground_color)
        left.setTextPen(foreground_color)
        bottom = self.plot_widget.getAxis("bottom")
        bottom.setPen(foreground_color)
        bottom.setTextPen(foreground_color)
        right = self.plot_widget.getAxis("right")
        right.setPen(foreground_color)
        right.setTextPen(background_color)
        self.plot_widget.getAxis("top").setPen(foreground_color)
        left.label.setDefaultTextColor(foreground_color)
        bottom.label.setDefaultTextColor(foreground_color)
        for text_item in self.text_items:
            text_item.setColor(foreground_color)
        self.legend.setLabelTextColor(foreground_color)
        self.legend.setBrush(background_color)
        self.legend.clear()
        if self.text_items:
            self.text_parent.opts = {
                "pen": foreground_color,
                "clipToView": False,
                "dynamicRangeLimit": 1e6,
                "autoDownsample": False,
            }
            self.legend.addItem(self.text_parent, name="Подписи элементов")
            self.legend.setPen(foreground_color)
        else:
            self.legend.setPen(background_color)

    def clear(self):
        """Отчищает виджеты."""

        self.plot_widget.clear()
        self.scatter.clear()
        self.text_items = []

    def plot(
        self,
        x_without_nan,
        y_without_nan,
        x_idx,
        a_plot,
        b_plot,
        names,
        x_label,
        y_label,
        title,
        is_light_theme=True,
    ):
        """Рисует кросс-плот."""

        self.is_light_theme = is_light_theme
        self.title = title
        self.text_items = []

        if len(x_without_nan) > 0:
            self.plot_widget.plot(
                x_without_nan[:, x_idx],
                x_without_nan[:, x_idx] * a_plot + b_plot,
                pen="b",
            )
            self.scatter.setData(x_without_nan[:, x_idx], y_without_nan)
            self.text_parent = self.plot_widget.plot(
                pen="black", name="Подписи элементов"
            )
            for i in range(x_without_nan.shape[0]):
                if self.is_light_theme:
                    text_color = "black"
                else:
                    text_color = "white"
                text_item = TextItem(
                    text=names[i],
                    anchor=(0.5, 0),
                    color=text_color,
                )
                text_item.setPos(x_without_nan[i, x_idx], y_without_nan[i])
                text_item.setParentItem(self.text_parent)
                self.text_items.append(text_item)
            self.plot_widget.addItem(self.scatter)
        self.plot_widget.setXRange(
            np.min(x_without_nan[:, x_idx]),
            np.max(x_without_nan[:, x_idx]),
        )
        self.plot_widget.setYRange(
            np.min(y_without_nan),
            np.max(y_without_nan),
        )
        self.plot_widget.getPlotItem().getViewBox().setAspectLocked(lock=True, ratio=1)
        rect = self.plot_widget.viewRect()
        self.plot_widget.getPlotItem().getViewBox().setAspectLocked(lock=False, ratio=1)
        self.plot_widget.setRange(rect)
        self.plot_widget.setMouseEnabled(True, True)
        self.plot_widget.setLabel(axis="left", text=y_label, **{"font-size": "13pt"})
        self.plot_widget.setLabel(axis="bottom", text=x_label, **{"font-size": "13pt"})
        self.set_colors(self.is_light_theme)
