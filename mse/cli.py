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


def read_file_or_stdin(in_file):
    if in_file == "-":
        data = sys.stdin.readlines()
        return " ".join(data)
    else:
        with open(in_file, "r") as f:
            data = f.read().replace("\n", "")
        return data


def make_estimations(table, row_sizes, quiet):
    estimator = InnoDBEstimator(table)
    estimator.estimate(row_counts=row_sizes, print_details=not quiet)


def main():
    arg = docopt(__doc__)

    parser = Parser()

    table = None

    # ----- READ TABLE -----
    if arg.get("dummy"):
        table = Table("dummy")
    elif arg.get("file"):
        sql_string = read_file_or_stdin(arg.get('INPUT'))
        table = parser.parse_table(sql_string)

    # ----- ADD CUSTOM COLUMNS -----
    if arg.get("--column"):
        for column_string in arg.get("--column"):
            column = parser.parse_column(column_string)
            table.add_or_update_column(column)

    # ----- ADD CUSTOM INDICES -----
    for index_string in arg.get("--index"):
        index = parser.parse_index(index_string)
        table.add_or_update_index(index)

    # ----- CHANGE DEFAULT CHARSET / COLLATION -----
    if arg.get("--charset") or arg.get("--collation"):
        charset, collation = fix_charset_collation(arg.get("--charset"), arg.get("--collation"))
        table.charset = charset
        table.collation = collation

    row_sizes = [int(size) for size in arg.get("--row-size")]
    make_estimations(table, row_sizes, arg.get('--quiet'))