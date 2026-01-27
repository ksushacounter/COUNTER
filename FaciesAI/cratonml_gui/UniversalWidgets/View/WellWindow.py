import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QWidget
from pyqtgraph import AxisItem, TextItem, mkPen, ColorBarItem, ImageItem, PlotWidget

from cratonml_gui.utilities.view_utilities import get_colors, set_colormap

CURVE_NAN_VALUE = -999.25
MAX_DEPTH_RANGE_IN_WINDOW = 65
X_LIM = [-1, 0, 0.75, 20, 23]
SPACE_BETWEEN_CONTAINERS = 0.25
Y_TOP_OFFSET = 0.025
STRAT_LEVEL_NAME_POS = -0.2
FONT_SIZE = 11


class WellWindow(QWidget):
    def __init__(
        self,
        curves,
        depths,
        labels,
        names,
        colors,
        logs,
        priority,
        labels_before_proc,
        strat_levels_names,
        strat_levels_depths,
        auto_scaling,
        manual_scaling_interval,
        manual_scaling_step,
        scaling_interval,
        is_light_theme=True,
    ):
        super(WellWindow, self).__init__()
        self.names = names
        self.colors = colors
        self.logs = logs
        self.priority = priority
        self.auto_scaling = auto_scaling
        self.manual_scaling_interval = manual_scaling_interval
        self.manual_scaling_step = manual_scaling_step
        self.scaling_interval = scaling_interval
        self.is_light_theme = is_light_theme
        self.prepare_data(
            curves=curves,
            depths=depths,
            labels=labels,
            labels_before_proc=labels_before_proc,
            strat_levels_names=strat_levels_names,
            strat_levels_depths=strat_levels_depths,
        )
        self.font = QFont()
        self.font.setPointSize(FONT_SIZE)

        self.layout = QHBoxLayout()
        self.plot()

    def prepare_data(
        self,
        curves,
        depths,
        labels,
        labels_before_proc,
        strat_levels_names,
        strat_levels_depths,
    ):
        mask = labels == CURVE_NAN_VALUE
        depths_without_nan = depths[~mask]
        self.min_depth = np.min(depths_without_nan)
        self.max_depth = np.max(depths_without_nan)
        min_idx = np.where(depths == self.min_depth)[0][0]
        max_idx = np.where(depths == self.max_depth)[0][0]
        self.cut_curves = curves[min_idx : max_idx + 1]
        self.cut_depths = depths[min_idx : max_idx + 1]

        labels_with_nan = np.zeros(len(labels))
        labels_with_nan[mask] = np.nan
        labels_with_nan[~mask] = labels[~mask]
        labels_with_nan = labels_with_nan[:, None]
        self.cut_labels = labels_with_nan[min_idx : max_idx + 1]

        self.n_clusters = np.unique(labels_with_nan[~np.isnan(labels_with_nan)]).shape[
            0
        ]

        labels_before_proc_with_nan = np.zeros(len(labels))
        labels_before_proc_with_nan[mask] = np.nan
        labels_before_proc_with_nan[~mask] = labels_before_proc
        if np.unique(labels_before_proc).size == 2:
            labels_before_proc_with_nan[~mask] = abs(labels_before_proc - 1)
        labels_before_proc_with_nan = labels_before_proc_with_nan[:, None]
        self.cut_labels_before_proc = labels_before_proc_with_nan[min_idx : max_idx + 1]

        idxs1 = np.where(self.min_depth <= strat_levels_depths)[0]
        idxs2 = np.where(strat_levels_depths <= np.rint(self.max_depth))[0]
        idxs = [i for i in idxs1 if i in idxs2]
        self.strat_levels_names = np.array(strat_levels_names)[idxs]
        self.strat_levels_depths = np.array(strat_levels_depths)[idxs]

    def set_colors(self, is_light):
        foreground_color, background_color = get_colors(is_light)
        self.widget.setBackground(None)
        self.widget.setTitle("Кривые", color=foreground_color, size="13pt")

        left = self.widget.getAxis("left")
        left.setPen(foreground_color)
        left.setTextPen(foreground_color)
        left.setStyle(hideOverlappingLabels=False)
        bottom = self.widget.getAxis("bottom")
        bottom.setPen(foreground_color)
        bottom.setTextPen(background_color)
        bottom.setStyle(hideOverlappingLabels=False)
        right = self.widget.getAxis("right")
        right.setPen(foreground_color)
        right.setTextPen(background_color)
        right.setStyle(hideOverlappingLabels=False)
        self.widget.getAxis("top").setPen(foreground_color)
        left.label.setDefaultTextColor(foreground_color)

        self.legend.setLabelTextColor(foreground_color)
        self.legend.setBrush(background_color)
        self.legend.clear()
        self.legend.addItem(self.img_res, name="Результат интерпретации")
        self.legend.addItem(self.img_res_before_proc, name="Результат до обработки")
        self.legend.addItem(self.img_background, name="Фон")
        for i in range(len(self.widget_curves)):
            self.legend.addItem(self.widget_curves[i], name=self.names[i])
        for line in self.lines:
            line.setPen(mkPen(color=foreground_color, width=1, style=Qt.DashLine))
        self.lines_parent.opts["pen"] = mkPen(
            color=foreground_color, width=1, style=Qt.DashLine
        )
        self.legend.addItem(self.lines_parent, name="Границы классов")

        self.colorbar_axis.setTextPen(foreground_color)

    def prepare_curves_for_plot(self):
        new_curves = []
        idx_several_parts_curves = []
        normalized_curves = []
        min_val = []
        max_val = []
        for i in range(self.cut_curves.shape[1]):
            curve = self.cut_curves[:, i]
            if self.auto_scaling[i]:
                min_val.append(self.scaling_interval[i][0])
                max_val.append(self.scaling_interval[i][1])
            else:
                min_val.append(self.manual_scaling_interval[i][0])
                max_val.append(self.manual_scaling_interval[i][1])
            if self.logs[i]:
                curve = np.log10(
                    self.cut_curves[:, i] + np.nanmin(self.cut_curves[:, i]) + 0.01
                )
                min_val[i] = np.log10(
                    min_val[i] + np.nanmin(self.cut_curves[:, i]) + 0.01
                )
                max_val[i] = np.log10(
                    max_val[i] + np.nanmin(self.cut_curves[:, i]) + 0.01
                )
            normalized_curves.append(curve - min_val[i])
            if not self.auto_scaling[i]:
                mask = normalized_curves[i] <= max_val[i]
                if len(np.unique(mask)) == 2:
                    idx_several_parts_curves.append(i)
                normalized_curves[i][mask] /= max_val[i] - min_val[i]
                curve_ = normalized_curves[i].copy()
                curve_[~mask] = np.nan
                new_curves.append(
                    (curve_ * self.container_x_length)
                    + X_LIM[2]
                    + SPACE_BETWEEN_CONTAINERS
                    * (np.where(self.containers == self.priority[i])[0][0] + 1)
                    + self.container_x_length
                    * np.where(self.containers == self.priority[i])[0][0]
                )
            else:
                normalized_curves[i] /= max_val[i] - min_val[i]
                new_curves.append(
                    (normalized_curves[i] * self.container_x_length)
                    + X_LIM[2]
                    + SPACE_BETWEEN_CONTAINERS
                    * (np.where(self.containers == self.priority[i])[0][0] + 1)
                    + self.container_x_length
                    * np.where(self.containers == self.priority[i])[0][0]
                )
        return (
            new_curves,
            idx_several_parts_curves,
            normalized_curves,
            min_val,
            max_val,
        )

    def plot_curves(self):
        self.containers = np.unique(self.priority)
        self.container_x_length = (
            X_LIM[3]
            - X_LIM[2]
            - SPACE_BETWEEN_CONTAINERS * max(3, self.containers.shape[0])
        ) / max(3, self.containers.shape[0])
        (new_curves, idx_several_parts_curves, normalized_curves, min_val, max_val) = (
            self.prepare_curves_for_plot()
        )

        pens = {
            "pen": [
                mkPen(color=tuple(i * 255 for i in self.colors[col]), width=2)
                for col in range(self.cut_curves.shape[1])
            ]
        }
        names = {"name": self.names}
        self.widget_curves = self.widget.multiDataPlot(
            x=new_curves, y=self.cut_depths, **pens, **names
        )
        for i in idx_several_parts_curves:
            k = 0
            while 1:
                if k == 0:
                    val = max_val[i] * self.manual_scaling_step[i]
                    mask = (normalized_curves[i] > max_val[i]) & (
                        normalized_curves[i] <= val
                    )
                else:
                    val = max_val[i] * k * self.manual_scaling_step[i]
                    mask = (
                        normalized_curves[i]
                        > max_val[i] * (k - 1) * self.manual_scaling_step[i]
                    ) & (normalized_curves[i] <= val)
                if len(np.unique(mask)) == 1:
                    break
                k += 1
                curve_ = normalized_curves[i].copy()
                curve_[mask] = (
                    (
                        normalized_curves[i][mask]
                        / (val - min_val[i])
                        * self.container_x_length
                    )
                    + X_LIM[2]
                    + SPACE_BETWEEN_CONTAINERS
                    * (np.where(self.containers == self.priority[i])[0][0] + 1)
                    + self.container_x_length
                    * np.where(self.containers == self.priority[i])[0][0]
                )
                curve_[~mask] = np.nan
                widget_curve = self.widget.plot(
                    x=curve_, y=self.cut_depths, pen=pens["pen"][i]
                )
                widget_curve.setParentItem(self.widget_curves[i])
        for i in range(len(self.widget_curves)):
            self.widget_curves[i].opts["pen"] = pens["pen"][i]
            self.widget_curves[i].setCurveClickable(True, width=10)

    def plot_result_images(self):
        self.img_res = ImageItem(self.cut_labels.T)
        self.img_res_before_proc = ImageItem(self.cut_labels_before_proc.T)
        self.img_background = ImageItem(self.cut_labels.T, **{"opacity": 0.2})
        self.img_res.setRect(
            X_LIM[1], self.min_depth, X_LIM[2], self.max_depth - self.min_depth
        )
        self.img_res_before_proc.setRect(
            X_LIM[1], self.min_depth, X_LIM[2], self.max_depth - self.min_depth
        )
        self.img_background.setRect(
            X_LIM[2],
            self.min_depth,
            X_LIM[3] - X_LIM[2],
            self.max_depth - self.min_depth,
        )
        self.img_res.opts = {"pen": mkPen(color="blue", width=10)}
        self.img_res_before_proc.opts = {"pen": mkPen(color="green", width=10)}
        self.img_background.opts = {"pen": mkPen(color="red", width=10)}

        self.widget.addItem(self.img_res_before_proc)
        self.widget.addItem(self.img_res)
        self.widget.addItem(self.img_background)

        color_map, _ = set_colormap(cmap_name="YlOrRd", n_pts=self.n_clusters)
        colorbar = ColorBarItem(
            colorMap=color_map, values=(-0.5, self.n_clusters - 0.5)
        )
        self.colorbar_axis = colorbar.getAxis("right")
        self.colorbar_axis.setTickFont(self.font)
        self.colorbar_axis.setTicks([[(i, str(i)) for i in range(self.n_clusters)]])
        self.colorbar_axis.setStyle(tickLength=5)
        colorbar.setImageItem(self.img_res, insert_in=self.widget.getPlotItem())
        colorbar.setImageItem(self.img_background, insert_in=self.widget.getPlotItem())
        colorbar.setImageItem(
            self.img_res_before_proc, insert_in=self.widget.getPlotItem()
        )

    def plot_border_lines(self):
        shift_labels = np.empty(self.cut_labels.shape)
        shift_labels[1:] = self.cut_labels[:-1]
        shift_labels[0] = self.cut_labels[0]
        idxs = np.where(self.cut_labels - shift_labels != 0)[0]
        self.lines_parent = self.widget.plot(
            name="lines", pen=mkPen(color="red", width=1, style=Qt.DashLine)
        )
        self.lines = []
        for i in idxs:
            line = self.widget.plot(
                x=[X_LIM[1], X_LIM[3]],
                y=[self.cut_depths[i], self.cut_depths[i]],
                pen=mkPen(color="black", width=1, style=Qt.DashLine),
            )
            line.setParentItem(self.lines_parent)
            self.lines.append(line)

    def plot_strat_levels_names(self):
        for i in range(len(self.strat_levels_names)):
            self.widget.plot(
                x=[STRAT_LEVEL_NAME_POS, X_LIM[1]],
                y=[self.strat_levels_depths[i], self.strat_levels_depths[i]],
                pen="red",
            )
            text = TextItem(text=self.strat_levels_names[i], color="red", anchor=(1, 1))
            text.setPos(STRAT_LEVEL_NAME_POS, self.strat_levels_depths[i])
            text.setFont(self.font)
            self.widget.addItem(text)

    def plot(self):
        self.widget = PlotWidget()
        self.widget.setMouseEnabled(False, True)
        self.legend = self.widget.addLegend(
            labelTextColor="black",
            labelTextSize="11pt",
            pen="gray",
            offset=(0, 1),
            brush="green",
        )

        self.plot_curves()

        self.widget.invertY(True)
        dh = min(MAX_DEPTH_RANGE_IN_WINDOW, self.max_depth - self.min_depth)
        y_lim = [self.min_depth - Y_TOP_OFFSET * dh, self.min_depth + dh]
        self.widget.setYRange(y_lim[1], y_lim[0], padding=0)
        self.widget.setXRange(X_LIM[0], X_LIM[-1], padding=0)

        self.plot_result_images()
        self.plot_border_lines()
        self.plot_strat_levels_names()

        axis_left = AxisItem(orientation="left", hideOverlappingLabels=True)
        axis_left.setTickFont(self.font)
        axis_left.setStyle(hideOverlappingLabels=True)
        axis_bottom = AxisItem(orientation="bottom", hideOverlappingLabels=True)
        axis_bottom.setTickFont(self.font)
        axis_bottom.setStyle(hideOverlappingLabels=True)
        axis_right = AxisItem(
            orientation="right", tickPen=mkPen(width=1e-10), hideOverlappingLabels=True
        )
        axis_right.setStyle(hideOverlappingLabels=True)
        axis_top = AxisItem(
            orientation="top",
            tickPen=mkPen(width=1e-10),
            showValues=False,
            hideOverlappingLabels=True,
        )
        axis_top.setStyle(hideOverlappingLabels=True)
        self.widget.setAxisItems(
            {
                "left": axis_left,
                "bottom": axis_bottom,
                "right": axis_right,
                "top": axis_top,
            }
        )
        self.widget.setLabel(axis="left", text="Глубина, м", **{"font-size": "13pt"})
        self.widget.showGrid(x=True, y=True, alpha=0.35)
        self.set_colors(self.is_light_theme)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)
