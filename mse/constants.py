# -*- coding: utf-8 -*-
import math

DEFAULT_CHARSET = 'latin1'

DEFAULT_STRING_TYPE_LENGTHS = {
    'CHAR': 1,
    'BINARY': 255,
    'VARCHAR': 255,
    'VARBINARY': 255,
    'TINYBLOB': 256,
    'TINYTEXT': 256,
    'BLOB': 512,
    'TEXT': 2 ** 16,
    'MEDIUMBLOB': 2 ** 24,
    'MEDIUMTEXT': 2 ** 32,
    'LONGBLOB': 2 ** 32,
    'LONGTEXT': 2 ** 24,
    'ENUM': 2 ** 8,
    'SET': 4,

}


def str_formula(adder):
    return lambda l, c: (l * c) + adder


def fixed(num):
    return lambda _l: num

# tuple(sane default length / formula(length, charset) -> size)
STRING_TYPES = {
    'CHAR': str_formula(0),
    'BINARY': str_formula(0),
    'VARCHAR': lambda l, c: (l * c) + 1 if l < 256 else (l * c) + 2,
    'VARBINARY': lambda l, c: (l * c) + 1 if l < 256 else (l * c) + 2,
    'TINYBLOB': str_formula(1),
    'TINYTEXT': str_formula(1),
    'BLOB': str_formula(2),
    'TEXT': str_formula(2),
    'MEDIUMBLOB': str_formula(3),
    'MEDIUMTEXT': str_formula(3),
    'LONGBLOB': str_formula(4),
    'LONGTEXT': str_formula(4),
    'ENUM': lambda l, _c: 1 if l <= 2 ** 8 else 2,
    'SET': lambda l, _c: int(math.log(l, 2))
}

# formula(length) -> size
NUMERIC_TYPES = {
    'BIT': lambda l: int((l + 7) / 8),
    'TINYINT': fixed(1),
    'SMALLINT': fixed(2),
    'MEDIUMINT': fixed(3),
    'INT': fixed(4),
    'INTEGER': fixed(4),
    'BIGINT': fixed(8),
    'DOUBLE': fixed(8),
    'REAL': fixed(8),
    'FLOAT': lambda l: 4 if (l <= 24) else 8,
    'DECIMAL': fixed(4),  # TODO:fix decimal formula
}

# formula(length) -> size
DATE_TYPES = {
    'DATE': fixed(3),
    'TIME': fixed(3),
    'DATETIME': fixed(8),
    'TIMESTAMP': fixed(4),
    'YEAR': fixed(1),
}