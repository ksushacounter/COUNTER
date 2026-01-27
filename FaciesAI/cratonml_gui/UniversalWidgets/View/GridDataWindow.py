import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QWidget
from pyqtgraph import (
    mkPen,
    AxisItem,
    PlotWidget,
    ColorBarItem,
    ImageItem,
    ScatterPlotItem,
    mkBrush,
    PlotCurveItem,
    ColorMap,
)

from cratonml_gui.utilities.view_utilities import get_colors, set_colormap, get_cmap

FONT_SIZE = 11
CENTROIDS_WIDGET_WIDTH = 50


class GridDataWindow(QWidget):
    """Класс для визуализации грида."""

    def __init__(
        self,
        grid,
        mask,
        x,
        y,
        is_light_theme=True,
        title=None,
        levels=None,
        uniq_labels=None,
        centroids=None,
        cmap="turbo",
        grid_legend="Результат",
        only_grid_visible=False,
        classic_colorbar=False,
    ):
        super(GridDataWindow, self).__init__()
        self.original_grid = grid
        self.xx = x
        self.yy = y
        self.levels = levels
        self.uniq_labels = uniq_labels
        self.centroids = centroids
        self.cmap = cmap
        self.title = title
        self.grid_legend = grid_legend
        self.only_grid_visible = only_grid_visible
        self.classic_colorbar = classic_colorbar
        self.is_light_theme = is_light_theme
        self.scatter = None
        self.polygons = []
        self.polygon_names = []
        self.polygon_ids = []
        self.images = []

        if len(np.unique(mask)) == 2 or np.unique(mask)[0]:
            self.original_grid[mask] = np.nan
        if self.uniq_labels is None:
            self.uniq_labels = np.unique(self.original_grid[~mask]).astype(int)
        if self.levels is None:
            self.levels = len(self.uniq_labels)
        self.grid = self.original_grid.copy()
        if not classic_colorbar:
            for val in range(self.levels):
                self.grid[np.where(self.grid == self.uniq_labels[val])[0]] = val
        self.grid_reshape = np.reshape(self.grid, self.xx.shape).T

        self.plot()

    def add_polygon(self, coordinates, polygon_id, polygon_name="polygon"):
        """Рисует полигон."""

        if len(coordinates) < 2:
            polygon = ScatterPlotItem(
                coordinates[:, 0],
                coordinates[:, 1],
                brush=mkBrush("black", width=2),
                pen=mkPen("black"),
            )
        else:
            polygon = PlotCurveItem(coordinates[:, 0], coordinates[:, 1])
            polygon.setPen(mkPen(color="black", width=3, style=Qt.DashLine))
        self.widget.addItem(polygon)
        if polygon_id not in self.polygon_ids:
            self.polygon_names.append(polygon_name)
            self.polygon_ids.append(polygon_id)
            self.polygons.append(polygon)
            self.legend.addItem(polygon, name=polygon_name)
        else:
            index = self.polygon_ids.index(polygon_id)
            polygon.setParentItem(self.polygons[index])
        self.set_colors(self.is_light_theme)

    def add_grids(self, grid, xx, yy, labels, polygon_label, cmap_name="turbo"):
        """Рисует дополнительный грид."""

        mask = np.isnan(grid)
        if mask.all():
            return
        curr_grid = grid
        curr_grid[~mask] = np.int32(grid[~mask])
        curr_grid[mask] = np.nan

        for val in range(len(labels)):
            curr_grid[np.where(curr_grid == labels[val])[0]] = val

        curr_grid_reshape = np.reshape(curr_grid, xx.shape).T
        img = ImageItem(curr_grid_reshape)
        img.setRect(
            np.min(xx), np.min(yy), np.max(xx) - np.min(xx), np.max(yy) - np.min(yy)
        )
        cmap = get_cmap(cmap_name)
        uniq_labels = np.unique(np.hstack((polygon_label, labels)))
        colors = cmap.getLookupTable(nPts=len(uniq_labels))
        img.setColorMap(
            ColorMap(
                pos=[0, 1],
                color=[
                    colors[np.where(polygon_label == uniq_labels)[0][0]],
                    colors[np.where(polygon_label == uniq_labels)[0][0]],
                ],
            )
        )
        self.widget.addItem(img)
        self.images.append(img)

    def delete_grids(self):
        """Удаляет все гриды, кроме основного."""

        for img in self.images:
            img.clear()
        self.images = []

    @staticmethod
    def tip(x, y, data):
        return str(data) + " (x: " + str(x) + ", y: " + str(y) + ")"

    def add_wells(self, coords, well_names):
        """Рисует скважины на гриде в виде точек."""

        self.scatter = ScatterPlotItem(
            pos=coords,
            name="Cкважины",
            size=10,
            brush=mkBrush(30, 255, 35, 255),
            hoverable=True,
            data=np.array(well_names),
            tip=GridDataWindow.tip,
        )
        self.widget.addItem(self.scatter)
        self.set_colors(self.is_light_theme)

    def set_colors(self, is_light):
        """Функция вызывается при смене темы. Меняет цвета всех элементов."""

        self.is_light_theme = is_light
        foreground_color, background_color = get_colors(is_light)
        self.widget.setBackground(None)

        self.widget.setTitle(self.title, color=foreground_color, size="13pt")

        left = self.widget.getAxis("left")
        left.setPen(foreground_color)
        left.setTextPen(foreground_color)
        bottom = self.widget.getAxis("bottom")
        bottom.setPen(foreground_color)
        bottom.setTextPen(foreground_color)
        self.widget.getAxis("right").setPen(foreground_color)
        self.widget.getAxis("top").setPen(foreground_color)

        bottom.label.setDefaultTextColor(foreground_color)
        left.label.setDefaultTextColor(foreground_color)

        if self.centroids is not None:
            self.centoids_widget.setBackground(None)
            self.centoids_widget.setTitle(" ", color=background_color)
            self.centoids_widget.getAxis("left").setPen(foreground_color)
            bottom = self.centoids_widget.getAxis("bottom")
            bottom.setPen(foreground_color)
            bottom.setTextPen(background_color)
            right = self.centoids_widget.getAxis("right")
            right.setPen(foreground_color)
            right.setTextPen(background_color)
            self.centoids_widget.getAxis("top").setPen(foreground_color)

            bottom.label.setDefaultTextColor(background_color)

        self.legend.setLabelTextColor(foreground_color)
        self.legend.setBrush(background_color)
        self.legend.clear()
        if self.grid_legend != "Результат":
            self.legend.addItem(self._main_img, name=self.grid_legend)
        if self.scatter is not None:
            self.legend.addItem(self.scatter, name="Cкважины")
        for i, polygon in enumerate(self.polygons):
            self.legend.addItem(polygon, name=self.polygon_names[i])
        if (
            self.grid_legend != "Результат"
            or self.scatter is not None
            or len(self.polygons) != 0
        ):
            self.legend.setPen(foreground_color)
        else:
            self.legend.setPen(background_color)

        self.colorbar_axis.setTextPen(foreground_color)
        self.colorbar_axis.setTickPen(foreground_color)

    def add_centroids(self):
        """Рисует центроиды."""

        self.centoids_widget = PlotWidget()
        self.centoids_widget.setMaximumWidth(CENTROIDS_WIDGET_WIDTH)
        y = np.linspace(
            0,
            1,
            self.centroids.shape[0]
            + 1
            + self.centroids.shape[0] * (self.centroids.shape[1] - 2),
        )
        for col in range(self.centroids.shape[0]):
            if col == 0:
                y_ = y[0 : self.centroids.shape[1]]
            else:
                y_ = y[
                    col
                    * (self.centroids.shape[1] - 1) : col
                    * (self.centroids.shape[1] - 1)
                    + self.centroids.shape[1]
                ]
            min_val = np.nanmin(self.centroids[col])
            max_val = np.nanmax(self.centroids[col])
            if max_val != min_val:
                self.centoids_widget.plot(
                    (self.centroids[col] - min_val) / (max_val - min_val),
                    y_,
                    pen=mkPen(color=self.colors[col], width=3),
                )
            else:
                self.centoids_widget.plot(
                    self.centroids[col], y_, pen=mkPen(color=self.colors[col], width=3)
                )
        self.centoids_widget.autoRange(padding=0)
        self.centoids_widget.setMouseEnabled(False, False)
        self.centoids_widget.hideButtons()

        axis_left = AxisItem(
            orientation="left", tickPen=mkPen(width=1e-10), showValues=False
        )
        axis_bottom = AxisItem(orientation="bottom", tickPen=mkPen(width=1e-10))
        axis_right = AxisItem(orientation="right", tickPen=mkPen(width=1e-10))
        axis_top = AxisItem(
            orientation="top", tickPen=mkPen(width=1e-10), showValues=False
        )
        self.centoids_widget.setAxisItems(
            {
                "left": axis_left,
                "bottom": axis_bottom,
                "right": axis_right,
                "top": axis_top,
            }
        )
        self.centoids_widget.setLabel(axis="bottom", text="A", **{"font-size": "13pt"})

    def plot(self):
        """Рисует грид."""

        self.widget = PlotWidget()
        self.legend = self.widget.addLegend(
            labelTextColor="black", labelTextSize="11pt", offset=(1, 1), brush="white"
        )
        self._main_img = ImageItem(self.grid_reshape)
        self.widget.addItem(self._main_img)
        self._main_img.opts = {"pen": "red"}
        self.legend.addItem(self._main_img, name=self.grid_legend)

        self.font = QFont()
        self.font.setPointSize(FONT_SIZE)

        if self.classic_colorbar:
            self.colorbar = ColorBarItem(colorMap=self.cmap)
        else:
            self.color_map, self.colors = set_colormap(
                cmap_name=self.cmap, n_pts=self.levels
            )
            self.colorbar = ColorBarItem(
                colorMap=self.color_map, values=(-0.5, self.levels - 0.5)
            )
        self.colorbar_axis = self.colorbar.getAxis("right")
        self.colorbar_axis.setTickFont(self.font)
        if not self.classic_colorbar:
            self.colorbar_axis.setTicks(
                [[(i, str(int(self.uniq_labels[i]))) for i in range(self.levels)]]
            )
        self.colorbar_axis.setStyle(tickLength=5)
        self.colorbar.setImageItem(self._main_img, insert_in=self.widget.getPlotItem())

        self.widget.setXRange(np.min(self.xx), np.max(self.xx))
        self.widget.setYRange(np.min(self.yy), np.max(self.yy))
        if self.only_grid_visible:
            mask = np.isnan(self.grid_reshape.T)
            self.widget.setXRange(np.min(self.xx[~mask]), np.max(self.xx[~mask]))
            self.widget.setYRange(np.min(self.yy[~mask]), np.max(self.yy[~mask]))

        self._main_img.setRect(
            np.min(self.xx),
            np.min(self.yy),
            np.max(self.xx) - np.min(self.xx),
            np.max(self.yy) - np.min(self.yy),
        )

        axis_left = AxisItem(orientation="left")
        axis_left.setTickFont(self.font)
        axis_bottom = AxisItem(orientation="bottom")
        axis_bottom.setTickFont(self.font)
        axis_right = AxisItem(orientation="right", showValues=False)
        axis_top = AxisItem(orientation="top", showValues=False)
        self.widget.setAxisItems(
            {
                "left": axis_left,
                "bottom": axis_bottom,
                "right": axis_right,
                "top": axis_top,
            }
        )
        self.widget.setLabel(axis="bottom", text="X, м", **{"font-size": "13pt"})
        self.widget.setLabel(axis="left", text="Y, м", **{"font-size": "13pt"})
        self.widget.getPlotItem().getViewBox().setAspectLocked(ratio=1)
        if self.centroids is not None:
            self.add_centroids()
        self.set_colors(self.is_light_theme)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.widget, Qt.AlignRight)
        if self.centroids is not None:
            self.layout.addWidget(self.centoids_widget)
        self.setLayout(self.layout)
