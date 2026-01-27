import numpy as np
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QWidget
from pyqtgraph import AxisItem, mkPen, ImageItem, ColorBarItem, PlotWidget

from cratonml_gui.utilities.view_utilities import set_colormap, get_colors

X_LIM = [-1, 20, 20.25]
WELLS_AMOUNT_TO_DISPLAY = 8
SPACE_BETWEEN_CONTAINERS = 0.25
FONT_SIZE = 11


class CurveClassesWindow(QWidget):
    def __init__(
        self,
        values,
        depths,
        classes,
        well_names,
        well_indexes,
        min_value,
        max_value,
        cmap="turbo",
        title=None,
        is_light_theme=True,
    ):
        super(CurveClassesWindow, self).__init__()
        self.values = values
        self.depths = depths
        self.classes = classes
        self.well_names = well_names
        self.well_indexes = well_indexes
        self.min_value = min_value
        self.max_value = max_value
        self.cmap = cmap
        self.title = title
        self.is_light_theme = is_light_theme

        self.layout = QHBoxLayout()
        self.font = QFont()
        self.font.setPointSize(FONT_SIZE)
        self.plot()

    def set_colors(self, is_light):
        foreground_color, background_color = get_colors(is_light)
        self.widget.setBackground(None)

        self.widget.setTitle(self.title, color=foreground_color, size="13pt")

        left = self.widget.getAxis("left")
        left.setPen(foreground_color)
        left.setTextPen(foreground_color)
        left.setTickPen(foreground_color)
        bottom = self.widget.getAxis("bottom")
        bottom.setPen(foreground_color)
        bottom.setTextPen(foreground_color)
        right = self.widget.getAxis("right")
        right.setPen(foreground_color)
        right.setTextPen(background_color)
        self.widget.getAxis("top").setPen(foreground_color)

        self.colorbar_axis.setTextPen(foreground_color)
        self.colorbar_axis.setTickPen(foreground_color)

    def plot(self):
        self.ncols = len(self.values)
        self.space_between_containers = SPACE_BETWEEN_CONTAINERS / (
            self.ncols / WELLS_AMOUNT_TO_DISPLAY
        )
        self.container_x_length = (
            X_LIM[1] - X_LIM[0] - self.space_between_containers * self.ncols
        ) / self.ncols

        self.widget = PlotWidget()
        all_labels = []
        for i in range(self.ncols):
            mask = np.isnan(self.values[i])
            all_labels.extend(np.unique(np.rint(self.values[i][~mask])))
        all_labels = np.unique(all_labels).astype(int)

        color_map, _ = set_colormap(cmap_name=self.cmap, n_pts=len(all_labels))
        colorbar = ColorBarItem(
            colorMap=color_map, values=(-0.5, len(all_labels) - 0.5)
        )
        self.colorbar_axis = colorbar.getAxis("right")
        self.colorbar_axis.setTickFont(self.font)
        self.colorbar_axis.setTicks(
            [[(i, str(all_labels[i])) for i in range(len(all_labels))]]
        )
        self.colorbar_axis.setStyle(tickLength=5)

        if len(self.well_indexes) == 0:
            self.well_indexes = np.arange(0, self.ncols)

        max_diff = 0
        ticks = []
        new_ticks = []
        x_lim = X_LIM[0] + self.space_between_containers
        for i in range(self.ncols):
            if i in self.well_indexes:
                curve = self.values[i].copy()
                curve = np.rint(curve)
                for val in range(len(all_labels)):
                    curve[np.where(self.values[i] == all_labels[val])[0]] = val
                self.img_res = ImageItem(curve.reshape(1, -1))
                self.img_res.setRect(
                    x_lim,
                    np.nanmin(self.depths[i]) - self.min_value[i],
                    self.container_x_length,
                    np.nanmax(self.depths[i]) - np.nanmin(self.depths[i]),
                )
                self.img_res.opts = {"pen": mkPen(color="blue", width=10)}
                self.widget.addItem(self.img_res)
                colorbar.setImageItem(self.img_res, insert_in=self.widget.getPlotItem())
                ticks.append(
                    (x_lim + self.container_x_length / 2, str(self.well_names[i]))
                )
                # new_ticks.append((x_lim + self.container_x_length / 2 , ''))
                x_lim += self.space_between_containers + self.container_x_length
                max_diff = max(max_diff, self.max_value[i] - self.min_value[i])

        x_lim = (
            X_LIM[0]
            + self.space_between_containers
            * (min(self.ncols, WELLS_AMOUNT_TO_DISPLAY) + 1)
            + self.container_x_length * min(self.ncols, WELLS_AMOUNT_TO_DISPLAY)
        )
        self.widget.setXRange(X_LIM[0], x_lim, padding=0)
        self.widget.setYRange(0, max_diff, padding=0)
        self.widget.invertY(True)
        self.layout.addWidget(self.widget)

        self.widget.setLabel(
            axis="left", text="Глубина от вер, м", **{"font-size": "13pt"}
        )
        axis_left = AxisItem(orientation="left", tickPen="black")
        axis_left.setTickFont(self.font)
        axis_bottom = AxisItem(orientation="bottom", tickPen=mkPen(width=1e-10))
        axis_bottom.setTickFont(self.font)
        axis_bottom.setTicks([ticks])

        # angle = 45
        # rotated_labels = []
        # for pos, label in ticks:
        #     label_item = LabelItem(label, angle=angle)
        #     rotated_labels.append((pos, label_item))
        # axis_bottom.setTicks([rotated_labels])

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

        self.set_colors(self.is_light_theme)
        self.setLayout(self.layout)
