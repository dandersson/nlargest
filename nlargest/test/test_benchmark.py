#!/usr/bin/env python3
import contextlib
import datetime
import io
import sys
import unittest

import benchmark as bench


@contextlib.contextmanager
def silence_stderr():
    """Context manager to keep sys.stderr silent."""
    class Devnull(object):
        def write(self, _): pass

        def flush(self): pass

    orig_stderr = sys.stderr
    sys.stderr = Devnull()
    try:
        yield
    finally:
        sys.stderr = orig_stderr


class TestTimeitCommand(unittest.TestCase):
    def test_full_command(self):
        setup = ['setup line 1', 'setup line 2']
        function = 'function call'
        expected = [
            'python3', '-m', 'timeit',
            '-s', setup[0],
            '-s', setup[1],
            function
        ]
        self.assertEqual(expected, bench.timeit_command(setup, function))

    def test_no_setup(self):
        setup = None
        function = 'function call'
        expected = [
            'python3', '-m', 'timeit',
            function
        ]
        self.assertEqual(expected, bench.timeit_command(setup, function))

    def test_no_function(self):
        setup = ['setup line 1', 'setup line 2']
        function = None
        with self.assertRaises(ValueError):
            bench.timeit_command(setup, function)


class TestTimeitOutputToFloat(unittest.TestCase):
    def test_valid_cases(self):
        mapping = [
            (('2.54', 'usec'), 2.54e-6),
            (('2.54', 'msec'), 2.54e-3),
            (('2.54', 'sec'), 2.54),
        ]
        for (time, time_unit), value in mapping:
            with self.subTest():
                self.assertEqual(
                    value,
                    bench.timeit_output_to_float(time, time_unit)
                )

    def test_bad_unit(self):
        with self.assertRaises(KeyError):
            bench.timeit_output_to_float('2.54', 'banana')

    def test_bad_number(self):
        with self.assertRaises(ValueError):
            bench.timeit_output_to_float('banana', 'sec')


class TestParseTimeitOutput(unittest.TestCase):
    def test_valid_cases(self):
        timeit_output_mapping = {
            '100000 loops, best of 3: 2.54 usec per loop': bench.TimeitResult(
                100000, 3, 2.54e-6
            ),
            '10000 loops, best of 5: 2.54 msec per loop': bench.TimeitResult(
                10000, 5, 2.54e-3
            ),
            '1000 loops, best of 7: 2.54 sec per loop': bench.TimeitResult(
                1000, 7, 2.54
            ),
        }
        for output, result in timeit_output_mapping.items():
            with self.subTest():
                self.assertEqual(result, bench.parse_timeit_output(output))


class TestGetFunctionNames(unittest.TestCase):
    def test_known_object_attr(self):
        prototype = type('', (), {})
        prefix = 'test_'
        names = ['nlargest1', 'nlargest2']
        attributes = [prefix + name for name in names]
        for key in attributes:
            setattr(prototype, key, True)
        self.assertEqual(
            attributes, bench.get_function_names(prototype, prefix)
        )


class TestSetupElement(unittest.TestCase):
    def test_string_interpolation(self):
        format_string = '{element_count}:{element_count}:{max_element_count}'
        format_args = {'element_count': 5, 'max_element_count': 10}
        expected = format_string.format(**format_args)
        self.assertEqual(
            expected, bench.setup_element(format_string, **format_args)
        )


class TestCLI(unittest.TestCase):
    file = '/dev/null'

    def test_config_argument(self):
        args = bench.parse_cli_arguments([self.file])
        self.assertEqual(self.file, args.config)
        with silence_stderr(), self.assertRaises(SystemExit):
            bench.parse_cli_arguments([])

    def test_save(self):
        args = bench.parse_cli_arguments([self.file])
        self.assertFalse(args.save)
        args = bench.parse_cli_arguments(['--save', self.file])
        self.assertTrue(args.save)

    def test_debug_argument(self):
        args = bench.parse_cli_arguments([self.file])
        self.assertFalse(args.debug)
        args = bench.parse_cli_arguments(['--debug', self.file])
        self.assertTrue(args.debug)


class TestConfigParser(unittest.TestCase):
    config_header = 'Benchmark'
    config_lines = {
        'powers': '1.0 1.2',
        'module_name': 'my_module',
        'prefix': 'my_prefix_',
        'setup': 'import this\n\timport that',
        'format_element': 'my_format_element',
        'format_call': 'my_format_call'
    }

    def mock_config(self):
        config_file = io.StringIO()
        config_file.write('[{}]\n'.format(self.config_header))
        config_file.write(
            '\n'.join(
                '{} = {}'.format(key, value)
                for key, value in self.config_lines.items()
            )
        )
        config_file.seek(0)
        return config_file

    def setUp(self):
        self.powers, self.module_name, self.prefix, self.setup, \
            self.format_element, self.format_call = \
            bench.parse_benchmark_configuration(self.mock_config())

    def test_powers(self):
        expected = list(map(float, self.config_lines['powers'].split()))
        self.assertEqual(expected, self.powers)

    def test_module_name(self):
        self.assertEqual(self.config_lines['module_name'], self.module_name)

    def test_prefix(self):
        self.assertEqual(self.config_lines['prefix'], self.prefix)

    def test_setup(self):
        expected = [
            line.lstrip('\t')
            for line in self.config_lines['setup'].split('\n')
        ]
        self.assertEqual(expected, self.setup)

    def test_format_element(self):
        self.assertEqual(
            self.config_lines['format_element'], self.format_element
        )

    def test_format_call(self):
        self.assertEqual(self.config_lines['format_call'], self.format_call)


class TestFilenameTimestamp(unittest.TestCase):
    time_format = '%Y-%m-%d_%H_%M_%S'

    def test_format_without_arguments(self):
        time = bench.filename_timestamp()
        try:
            datetime.datetime.strptime(time, self.time_format)
        except ValueError:
            self.fail('unexpected date format')

    def test_explicit_timestamp(self):
        timestamp = datetime.datetime(1975, 4, 9, 12, 34, 56)
        formatted_timestamp = timestamp.strftime(self.time_format)
        self.assertEqual(
            formatted_timestamp, bench.filename_timestamp(timestamp)
        )


if __name__ == '__main__':
    unittest.main()
