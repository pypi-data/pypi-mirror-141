import argparse
import json
import os.path
import sys
from enum import Enum
from typing import TextIO

from randalyze.analyzers import BenfordAnalyzer
from randalyze.generators import BenfordRandom


class OutputFormat(Enum):
    TEXT = 1
    JSON = 2
    CSV = 3


def check_percentage(value):
    percentage = float(value)

    if percentage < 0 or percentage > 100:
        raise argparse.ArgumentTypeError('%s in an invalid floating percentage value (0-100)' % percentage)

    return percentage


def parse_arguments():
    parser = argparse.ArgumentParser(description='Random number generator and analyzer.')

    subparsers = parser.add_subparsers(dest='command')

    generate_parser = subparsers.add_parser('generate',
                                            help='Generate a series of random numbers')

    generate_parser.add_argument('generator',
                                 choices=['benford'],
                                 default='benford',
                                 help='The type of generator to use')

    generate_parser.add_argument('-c', '--count',
                                 type=int,
                                 default=100,
                                 help='The number of values to generate')

    generate_parser.add_argument('-a', '--adjustments',
                                 type=int,
                                 default=5,
                                 help='The number of adjustments made to each generated number (default: %(default)s)'
                                 )

    generate_parser.add_argument('-f', '--format',
                                 choices=['text', 'json', 'csv'],
                                 default='text',
                                 help='The format of the output')

    analyze_parser = subparsers.add_parser('analyze',
                                           help='Analyze a series of random numbers')

    analyze_parser.add_argument('analyzer',
                                choices=['benford'],
                                default='benford',
                                help='The type of analyzer to use')

    analyze_parser.add_argument('--second-digit',
                                default=False,
                                action=argparse.BooleanOptionalAction,
                                help='Analyze and return details of second digits of the numbers passed to the analyzer.'
                                )

    analyze_parser.add_argument('-t', '--tolerance',
                                type=check_percentage,
                                default=5,
                                help='The pattern matching tolerance, in percent (default: %(default)s%%)')

    analyze_parser.add_argument('-f', '--format',
                                choices=['text', 'json'],
                                default='text',
                                help='The format of the output')

    analyze_parser.add_argument('input_file',
                                metavar='FILE',
                                nargs='?',
                                default='-',
                                help='The file to use as a source of numbers for analysis, or - for stdin.')

    return parser.parse_args()


# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def generator_function(generator, count: int):
    for _ in range(0, count):
        yield generator.random()


def generate_numbers(count: int, adjustments: int, output_format: OutputFormat) -> None:
    generator = BenfordRandom(adjustments=adjustments)

    start = ''
    separator = '\n'
    end = '\n'

    if output_format == OutputFormat.JSON:
        start = '['
        separator = ','
        end = ']'
    elif output_format == OutputFormat.CSV:
        start = 'numbers,\n'
        separator = ',\n'
        end = '\n'

    sys.stdout.write(start)

    index = 0
    for _ in generator_function(generator, count):
        sys.stdout.write('{}'.format(generator.random()))
        index += 1
        if index < count:
            sys.stdout.write(separator)

    sys.stdout.write(end)

    sys.stdout.flush()


def populate_analyzer(analyzer, source: TextIO) -> None:
    for line in source:
        try:
            value = float(line.strip())
            analyzer.add_number(value)
        except Exception as ex:
            print(f'Stuff: {ex}')


def main():
    arguments = parse_arguments()

    if arguments.command == 'generate':
        output_format = OutputFormat[arguments.format.upper()]
        generate_numbers(arguments.count, arguments.adjustments, output_format)

    elif arguments.command == 'analyze':
        analyzer = BenfordAnalyzer()

        output_format = OutputFormat[arguments.format.upper()]

        if arguments.input_file and arguments.input_file != '-':
            # Check the specified file exists
            if not os.path.isfile(arguments.input_file):
                raise IOError(f'Input file does not exist at: {arguments.input_file}')

        if not arguments.input_file or arguments.input_file == '-':
            populate_analyzer(analyzer, sys.stdin)
        else:
            with open(arguments.input_file, mode='r') as source:
                populate_analyzer(analyzer, source)

        if output_format == OutputFormat.JSON:
            benford_distribution = {'name': 'benford',
                                    'matches': analyzer.matches_distribution(arguments.tolerance),
                                    'first_digit': {
                                        'distribution': {i: analyzer.first_digit_distribution[i] for i
                                                         in range(10)},
                                        'counts': {i: analyzer.first_digit_counts[i] for i in
                                                   range(10)}
                                    }
                                    }

            if False and arguments.second_digit:
                benford_distribution['second_digit'] = {
                    'distribution': analyzer.second_digit_distribution,
                    'counts': analyzer.second_digit_counts,
                    'combined': {
                        'distribution': analyzer.second_digit_distribution_combined,
                        'counts': analyzer.second_digit_counts_combined
                    }
                }

            result = {'distributions': [benford_distribution]}
            sys.stdout.write(json.dumps(result))
            sys.stdout.flush()
        else:
            analyzer.write_text_report(arguments.tolerance)


if __name__ == '__main__':
    main()
