# -*- coding: utf-8 -*-
"""Mysql Size Estimator

Usage:
    mysql-size-estimator.py file [-c COLUMN]... [-i INDEX]... [-r ROW_SIZE]... [options] INPUT
    mysql-size-estimator.py dummy -c COLUMN [-c COLUMN]... [-i INDEX]... [-r ROW_SIZE]... [options]

Arguments:
    COLUMN     Column definition
    INDEX      Index definition
    CHARSET    Character set
    COLLATION  Character set collation
    INPUT      File or STDIN (use - for STDIN)

Options:
    -c COLUMN --column=COLUMN            Overwrite/Define column.
    -i INDEX --index=INDEX               Overwrite/Define index
    --charset=CHARSET                    Overwrite default charset for table
    --collation=COLLATION                Overwrite default collation for table
    -r ROW_SIZE --row-size ROW_SIZE      Row size for estimations
    -q --quiet                           Quiet, skip printing details

"""
import sys
from docopt import docopt
from .estimators import InnoDBEstimator
from .parser import Parser
from .base import Table
from .charset import fix_charset_collation


class CliParser:
    def __init__(self, args):
        self._parser = Parser()
        self.table = None
        self._parse_table(args)
        self.report_row_sizes = [int(size) for size in args.get("--row-size")]
        self.is_quiet = args.get('--quiet')

    def _parse_table(self, args):
        if args.get("dummy"):
            self._create_dummy_table()
        elif args.get("file"):
            if args.get("INPUT") == '-':
                self._read_table_from_stdin()
            else:
                self._read_table_from_file(args.get("INPUT"))
        self._update_columns(args)
        self._update_indexes(args)
        self._update_charset(args)

    def _create_dummy_table(self):
        self.table = Table("dummy")

    def _read_table_from_stdin(self):
        data = sys.stdin.readlines()
        table_str = " ".join(data)
        self.table = self._parser.parse_table(table_str)

    def _read_table_from_file(self, filename):
        with open(filename, "r") as f:
            table_str = f.read().replace("\n", "")
        self.table = self._parser.parse_table(table_str)

    def _update_columns(self, args):
        for column_string in args.get("--column"):
            column = self._parser.parse_column(column_string)
            self.table.add_or_update_column(column)

    def _update_indexes(self, args):
        for index_string in args.get("--index"):
            index = self._parser.parse_index(index_string)
            self.table.add_or_update_index(index)

    def _update_charset(self, args):
        if args.get("--charset") or args.get("--collation"):
            charset, collation = fix_charset_collation(args.get("--charset"), args.get("--collation"))
            self.table.charset = charset
            self.table.collation = collation


def make_estimations(table, row_sizes, quiet):
    estimator = InnoDBEstimator(table)
    estimator.estimate(row_counts=row_sizes, print_details=not quiet)


def main():
    args = docopt(__doc__)
    parsed = CliParser(args)
    make_estimations(parsed.table, parsed.report_row_sizes, parsed.is_quiet)
