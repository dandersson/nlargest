#!/usr/bin/env python3
"""Benchmark functions, print result to screen and optionally save to permanent
pickled storage."""
import argparse
import configparser
import functools
import importlib
import itertools
import logging
import os
import pickle
import subprocess
import sys
from collections import namedtuple
from datetime import datetime


DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(DIR, 'output')


TimeitResult = namedtuple('TimeitResult', 'loops repetitions time')


BenchmarkResult = namedtuple('BenchmarkResult',
                             'function element_count result')


def timeit_command(function_setup, function_call):
    """Build command suitable for the CLI of the timeit module."""
    if function_setup is None:
        function_setup = []
    if function_call is None:
        raise ValueError('no function defined for the Timeit module to run')

    setup = [item for setup in function_setup for item in ['-s', setup]]
    command = ['python3', '-m', 'timeit'] + setup + [function_call]
    return command


def timeit_output_to_float(time, time_unit):
    """Transform a timeit style output number with human readable unit to a
    float. Handle

    * "sec"     → s
    * "msec"    → ms
    * "usec"    → µs
    """
    exponent_translation = {'sec': '', 'msec': 'e-3', 'usec': 'e-6'}
    return float(time + exponent_translation[time_unit])


def parse_timeit_output(output):
    """Parse relevant information from timeit CLI output."""
    r_loops, _, _, _, r_repetitions, r_time, r_time_unit, *_ = output.split()
    loops = int(r_loops)
    repetitions = int(r_repetitions.rstrip(':'))
    time = timeit_output_to_float(r_time, r_time_unit)
    return TimeitResult(loops, repetitions, time)


def get_function_names(module, prefix):
    """Get function names with a certain prefix from a module."""
    return [fun for fun in dir(module) if fun.startswith(prefix)]


def setup_element(format_element, element_count, max_element_count):
    """Interpolate element specific setup string."""
    return format_element.format(
        max_element_count=max_element_count, element_count=element_count
    )


def filename_timestamp(timestamp=None):
    """Generate a timestamp suitable to specify a file."""
    if timestamp is None:
        timestamp = datetime.now()

    time_format = '%Y-%m-%d_%H_%M_%S'
    return timestamp.strftime(time_format)


def parse_cli_arguments(args):
    """Define CLI and parse arguments accordingly."""
    argparser = argparse.ArgumentParser(description=__doc__)

    argparser.add_argument('config', help='configuration file')
    argparser.add_argument('--save', action='store_true',
                           help='save output to permanent storage')
    argparser.add_argument('--debug', action='store_true',
                           help='enable debug output')

    return argparser.parse_args(args)


def configure_logging(level):
    """Configure local `logging` instance."""
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('invalid log level: {}'.format(level))
    logging.basicConfig(format=u'%(levelname)s: %(message)s',
                        level=numeric_level)


def parse_benchmark_configuration(file):
    """Parse fields from INI-style configuration file section "Benchmark".

    Parsed fields:
        powers: whitespace separated string of float representations.
        module_name: name of module to import for benchmarking.
        prefix: prefix for functions within the module to benchmark.
        setup: statements to be executed as the setup stage for Timeit.
        format_element: string sent to setup, with format interpolation for
            {element_count}: number of elements for a certain run.
            {element_count_max}: maximum number of elements during the run.
        format_call: string to be benchmarked, with format interpolation for
            {function}: name of the function being benchmarked.
    """
    cparser = configparser.ConfigParser()
    cparser.read_file(file)
    cget = functools.partial(cparser.get, 'Benchmark')

    powers = list(map(float, cget('powers').split()))
    module_name = cget('module_name')
    prefix = cget('prefix')
    setup = cget('setup').split('\n')
    format_element = cget('format_element')
    format_call = cget('format_call')

    return powers, module_name, prefix, setup, format_element, format_call


def main(cli_args):
    args = parse_cli_arguments(cli_args)
    configure_logging('DEBUG' if args.debug else 'INFO')
    with open(args.config) as file:
        powers, module_name, prefix, setup, format_element, format_call = \
            parse_benchmark_configuration(file)

    element_counts = [int(10**power) for power in powers]
    max_element_count = max(element_counts)

    def benchmark(function, element_count):
        element_setup = setup_element(
            format_element, element_count, max_element_count
        )
        call = format_call.format(function=function)

        command = timeit_command(setup + [element_setup], call)
        logging.debug("::".join(command))

        r_output = subprocess.check_output(command, universal_newlines=True)
        output = parse_timeit_output(r_output)

        result = BenchmarkResult(function, element_count, output)
        logging.info(result)
        return result

    module = importlib.import_module(module_name)
    function_names = get_function_names(module, prefix)

    logging.info('STARTING BENCHMARK RUN')
    logging.info(
        'Results will be saved to file' if args.save
        else 'Run with the --save option to save run results to file.'
    )
    logging.info('Functions:\n  {}'.format('\n  '.join(function_names)))
    logging.info('Element counts:\n  {}'.format(element_counts))

    results = [
        benchmark(function, element_count)
        for function, element_count
        in itertools.product(function_names, element_counts)
    ]

    if args.save:
        filename = 'benchmark_output_{}'.format(filename_timestamp())
        output_file = os.path.join(OUTPUT_DIR, filename)
        with open(output_file, 'wb') as f:
            pickle.dump(results, f)

        logging.info('Wrote benchmark results to "{}".'.format(output_file))


if __name__ == '__main__':
    main(sys.argv[1:])
