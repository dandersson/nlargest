#!/usr/bin/env python3
"""Utility functions for plotting benchmark results with Matplotlib."""
import collections
import matplotlib.pyplot as plt
import numpy as np
import pickle


# numpy column selectors.
X = slice(None), slice(0, 1)
Y = slice(None), slice(1, None)


def dict_of_numpy_data(f):
    """Load test results into a dictionary."""
    data = pickle.load(f)

    plot_series = collections.defaultdict(list)
    for function, element_count, (loops, repetition, time) in data:
        plot_series[function].append((element_count, time))
    return {k: np.array(v) for k, v in plot_series.items()}


def series_plotter(input_data, *, axis=None, compress_legend=False, save=False,
                   figure_path=None):
    """Prototype plotting function."""
    default_style = '-x'
    for (label, style), data in input_data:
        if style is None:
            style = default_style
        plt.loglog(data[X], data[Y], style, label=label)

    plt.suptitle('Performance metrics of nlargest functions (pick 5) for '
                 'fixed-seed randomized input data')
    plt.xlabel('Elements')
    plt.ylabel('Time $/$s')
    if axis is not None:
        plt.axis(axis)
    fontsize = 8 if compress_legend else 10
    plt.legend(fontsize=fontsize, loc='upper left', numpoints=1)
    if save:
        print('Saving output → {}'.format(figure_path))
        plt.savefig(figure_path, bbox_inches='tight')
    else:
        plt.show()
    plt.close()


def plot_all_series(data, **kwargs):
    """Plot all available series."""
    series_plotter(
        sorted(((k, None), data[k]) for k in data),
        compress_legend=True,
        **kwargs
    )


def plot_select_series(data, plot_series, **kwargs):
    """Plot series selected by name."""
    series_plotter(((k, data[k[0]]) for k in plot_series), **kwargs)
