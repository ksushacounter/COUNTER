import numpy as np
from pyqtgraph import colormap, ColorMap


def get_colors(is_light_theme):
    if is_light_theme:
        foreground_color = "black"
        background_color = "white"
    else:
        foreground_color = "#e0e1e3"
        background_color = "#19232d"
    return foreground_color, background_color


def get_cmap(cmap_name):
    cmap = None
    try:
        cmap = colormap.get(cmap_name)
    except:
        try:
            cmap = colormap.getFromMatplotlib(cmap_name)
        except:
            pass
    return cmap


def set_colormap(cmap_name, n_pts, negative=False):
    cmap = get_cmap(cmap_name)
    if cmap is not None:
        colors = cmap.getLookupTable(nPts=n_pts)
        if negative:
            colors = [(255 - c[0], 255 - c[1], 255 - c[2]) for c in colors]
        new_color = np.empty((n_pts * 2, 3))
        pos = np.empty((n_pts * 2,))
        for i in range(n_pts):
            new_color[2 * i] = colors[i]
            pos[2 * i] = 1 / n_pts * i
            new_color[2 * i + 1] = colors[i]
            pos[2 * i + 1] = 1 / n_pts * (i + 1) - 1e-10

        return ColorMap(pos=pos, color=new_color), colors
