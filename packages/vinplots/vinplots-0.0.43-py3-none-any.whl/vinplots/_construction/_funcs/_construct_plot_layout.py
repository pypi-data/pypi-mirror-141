from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import math

from ._default_matplotlib_figure_dimensions import _default_matplotlib_figure_dimensions

def _calculate_nrows(nplots, ncols):
    return math.ceil(nplots / ncols)

def _initialize_plot_with_dimensions(ncols, nrows, figsize_width, figsize_height):

    """
    Parameters:
    -----------
    ncols
        Number of columns in the figure.
        type: int
    nrows
        Number of rows in the figure.
        type: int
    figsize_width
        Scaler adjustment of figure width
        default: 1
        type: float
    figsize_height
        Scaler adjustment of figure height
        default: 1
        type: float
    Returns:
    --------
    fig
        type: matplotlib.figure.Figure
    Notes:
    ------
    """

    fig_dimensions = _default_matplotlib_figure_dimensions()*np.array([ncols * figsize_width, nrows * figsize_height])
    fig = plt.figure(figsize=fig_dimensions)

    return fig

def _construct_plot_layout(
    nplots,
    ncols=4,
    figsize_width=1,
    figsize_height=1,
    grid_hspace=0.2,
    grid_wspace=0,
    width_ratios=False,
    height_ratios=False,
):

    """
    Creates Axes for each desired plot.
    Parameters:
    -----------
    nplots
    ncols
        Number of columns. 
        default: 4
        type: int
    Returns:
    --------
    Notes:
    ------
    """

    if np.any(width_ratios) == False:
        if nplots <= ncols:
            width_ratios = np.ones(ncols)

    nrows = _calculate_nrows(nplots, ncols)
    
    if not height_ratios:
        height_ratios = np.ones(nrows)
            
    fig = _initialize_plot_with_dimensions(ncols, nrows, figsize_width, figsize_height)
    gridspec = GridSpec(nrows, 
                        ncols,
                        width_ratios=width_ratios,
                        height_ratios=height_ratios,
                        hspace=grid_hspace,
                        wspace=grid_wspace)

    plot_count = 0
    AxesDict = {}

    for ax_i in range(nrows):
        AxesDict[ax_i] = {}
        for ax_j in range(ncols):
            plot_count += 1
            AxesDict[ax_i][ax_j] = fig.add_subplot(gridspec[ax_i, ax_j])
            if plot_count >= nplots:
                break

    return fig, AxesDict