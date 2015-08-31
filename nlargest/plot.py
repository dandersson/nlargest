#!/usr/bin/env python3
"""Plot benchmark results."""
import argparse
import itertools
import os.path
import sys

from benchmark import BenchmarkResult, TimeitResult  # noqa
import plotter


def parse_cli_arguments(args):
    """Define CLI and parse arguments accordingly."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('file', help='benchmark data file', metavar='FILE')
    argparser.add_argument('--save', action='store_true',
                           help='save image files')
    argparser.add_argument('--figure-dir', metavar='DIR', default='figures',
                           help='figure output directory [default: figures]')
    return argparser.parse_args(args)


def plot_all_series(data, **kwargs):
    """Wrapper to plot all data series in a single plot."""
    plotter.plot_all_series(data, **kwargs)


def plot_init_1_against_init_2(data, **kwargs):
    """Plot initialisation method 1 against initialisation method 2."""
    plot_series = [
        ('nlargest_list', '-x'),
        ('nlargest_list2', '-x'),
        ('nlargest_heapreplace', '-o'),
        ('nlargest_heapreplace2', '-o'),
        ('nlargest_manual_heapreplace', '-v'),
        ('nlargest_manual_heapreplace2', '-v'),
        ('nlargest_heappushpop', '-s'),
        ('nlargest_heappushpop2', '-s'),
    ]
    plotter.plot_select_series(data, plot_series, **kwargs)


def plot_init_1_against_init_3(data, **kwargs):
    """Plot initialisation method 1 against initialisation method 3."""
    plot_series = [
        ('nlargest_list', '-x'),
        ('nlargest_list3', '-x'),
        ('nlargest_heapreplace', '-o'),
        ('nlargest_heapreplace3', '-o'),
        ('nlargest_manual_heapreplace', '-v'),
        ('nlargest_manual_heapreplace3', '-v'),
        ('nlargest_heappushpop', '-s'),
        ('nlargest_heappushpop3', '-s'),
    ]
    plotter.plot_select_series(data, plot_series, **kwargs)


def plot_init_2_against_init_3(data, **kwargs):
    """Plot initialisation method 2 against initialisation method 3."""
    plot_series = [
        ('nlargest_list2', '-x'),
        ('nlargest_list3', '-x'),
        ('nlargest_heapreplace2', '-o'),
        ('nlargest_heapreplace3', '-o'),
        ('nlargest_manual_heapreplace2', '-v'),
        ('nlargest_manual_heapreplace3', '-v'),
        ('nlargest_heappushpop2', '-s'),
        ('nlargest_heappushpop3', '-s'),
    ]
    plotter.plot_select_series(data, plot_series, **kwargs)


def plot_ref_against_init_2(data, **kwargs):
    """Plot reference implementations against initialisation method 2."""
    plot_series = [
        ('nlargest_ref_sorted', '-x'),
        ('nlargest_ref_heapq', '-x'),
        ('nlargest_list2', '-*'),
        ('nlargest_heapreplace2', '-o'),
        ('nlargest_manual_heapreplace2', '-v'),
        ('nlargest_heappushpop2', '-s'),
    ]
    plotter.plot_select_series(data, plot_series, **kwargs)


def main(cli_args):
    args = parse_cli_arguments(cli_args)

    with open(args.file, 'br') as f:
        plot_data = plotter.dict_of_numpy_data(f)

    axes = {
        'small': [1e1, 1e4, 1e-6, 4e-3],
        'large': [1e1, 1e7, 1e-6, 2e1],
    }

    plot_functions = (v for k, v in globals().items() if k.startswith('plot_'))

    filename = os.path.basename(args.file)
    for function, (axis_name, axis) \
            in itertools.product(plot_functions, axes.items()):
        figure_name = '{}__{}__axis_{}.png'.format(
            filename,
            function.__name__,
            axis_name
        )
        figure_path = os.path.join(args.figure_dir, figure_name)
        function(plot_data, axis=axis, save=args.save, figure_path=figure_path)


if __name__ == '__main__':
    main(sys.argv[1:])
