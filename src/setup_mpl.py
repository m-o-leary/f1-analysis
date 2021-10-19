from typing import Dict
import fastf1 as ff1
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
import numpy as np
import pandas as pd

def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)

    plt.sca(current_ax)
    
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=False,
                   labeltop=True, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", axis="x", color="black", linestyle='--', linewidth=1)
    ax.grid(which="minor", axis="y", color="black", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", top=False, left=False)

    return im

def plot_lap_heatmap(laps:pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(25,10), dpi=600)

    im = heatmap(
        laps.fillna(method='bfill').T.values, 
        laps.T.index, 
        laps.T.columns, 
        ax=ax,
        cmap="PRGn_r",
        interpolation="antialiased"
    )
    add_colorbar(im)
    plt.title("Cummulative Gap from To Reference")
    # plt.subtitle("Reference = mean of: all lap times within best lap + 10% accumulated over laps")
    plt.tight_layout()
    plt.show()

def plot_lap_gap(laps:pd.DataFrame, drivers_kw: Dict[str, Dict]) -> None:
    fig, ax = plt.subplots(figsize=(8,6), dpi=600)
    ax.grid(color='#2A3459')
    n_shades = 10
    diff_linewidth = 1.05
    alpha_value = 0.3 / n_shades

    teams = []
    for col in laps.columns.tolist():
        
        color = drivers_kw[col]["color"]
        driver_team = drivers_kw[col]["team"]

        if driver_team in teams:
            for n in range(1, n_shades+1):    
                laps[col].plot(
                    ax=ax, 
                    linewidth=2+(diff_linewidth*n), 
                    alpha=alpha_value,
                    color=color
                )
        else:
            laps[col].plot(
                ax=ax, 
                legend=False,
                lw=1.5, 
                color=color
            )
            teams.append(driver_team)
    ax.set_xticks(range(1,54))
    ax.tick_params(axis='both', which='major', labelsize=5)
    ax.tick_params(axis='both', which='minor', labelsize=4)

def make_driver_color_dict(file_loc:str)->Dict[str,Dict]:
    driver_meta = pd.read_csv(file_loc)
    drivers = driver_meta['driver_code'].values
    teams = driver_meta['team'].values
    colors = ff1.plotting.TEAM_COLORS
    return dict(
        zip(
            drivers, 
            [ dict(team=team, color=colors[team]) for team in teams ]))

def setup_mpl()->None:
    # Add every font at the specified location
    font_dir = ['/Users/martin/Library/Fonts']
    for font in matplotlib.font_manager.findSystemFonts(font_dir):
        matplotlib.font_manager.fontManager.addfont(font)

    # Set font family globally

    plt.style.use("seaborn-dark")
    matplotlib.rcParams['font.family'] = 'Formula1-Regular'
    matplotlib.rcParams["font.weight"] = "normal"
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        matplotlib.rcParams[param] = '#212946'  # bluish dark grey
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        matplotlib.rcParams[param] = '0.9'  # very light grey


    