# -*- coding: utf-8 -*-
"""Mysql Size Estimator

Usage:
    mysql-size-estimator.py [-c COLUMN]... [-i INDEX]... [-r ROW_SIZE]... [-q] INPUT
    mysql-size-estimator.py dummy -c COLUMN [-c COLUMN]... [-i INDEX]... [-r ROW_SIZE]... [-q]

Arguments:
    COLUMN  Column definition
    INDEX   Index definition
    INPUT   File or STDIN

Options:
    -c COLUMN --column=COLUMN         Overwrite/Define column.
    -i INDEX --index=INDEX            Overwrite/Define index
    -r ROW_SIZE --row-size ROW_SIZE   Row size for estimations
    -q --quiet                        Quiet, skip printing details

"""
import sys
from docopt import docopt
from .estimators import InnoDBEstimator
from .parser import Parser
from .base import Table



def read_file_or_stdin(in_file):
    if in_file == "-":
        data = sys.stdin.readlines()
        return " ".join(data)
    else:
        with open(in_file, "r") as f:
            data = f.read().replace("\n","")
        return data

def make_estimations(table, row_sizes, quiet):
    estimator = InnoDBEstimator(table)
    estimator.estimate(row_counts=row_sizes, print_details=not quiet)

def main():
    arg = docopt(__doc__)

    parser = Parser()

    if arg.get("dummy"):
        table = Table("dummy")
    else:
        sqlString = read_file_or_stdin(arg.get('INPUT'))
        table = parser.parse_table(sqlString)

    for column_string in arg.get("--column"):
        column = parser.parse_column(column_string)
        table.add_or_update_column(column)

    for index_string in arg.get("--index"):
        index = parser.parse_index(index_string)
        table.add_or_update_index(index)

    row_sizes = [int(size) for size in arg.get("--row-size")]
    make_estimations(table, row_sizes, arg.get('--quiet'))