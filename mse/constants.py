# -*- coding: utf-8 -*-
import math

# TODO: re-check all per character byte values (most of them are wrong)
CHARSET_SIZE_PER_CHAR = {
    # Unicode Character Sets
    'ucs2': 2,
    'utf16': 2,
    'utf32': 4,
    'utf8': 3,
    'utf8mb4': 4,  # TODO: this one uses 1-4 bytes but don't know how to put it in formula

    # West European Character Sets
    'ascii': 1,
    'cp850': 1,
    'dec8': 1,
    'hp8': 1,
    'latin1': 1,
    'macroman': 1,
    'swe7': 1,

    # Central European Character Sets
    'cp1250': 1,
    'cp852': 1,
    'latin2': 1,
    'macce': 1,

    # South European and Middle East Character Sets
    'armscii8': 1,
    'cp1256': 1,
    'geostd8': 1,
    'greek': 1,
    'hebrew': 1,
    'latin5': 1,

    # TODO : fill the rest

}

# tuple(default charset / default size / formula(length, charset) -> size)
STRING_TYPES = {
    'CHAR': ('latin1', 1, lambda l, c: l * c),
    'BINARY': ('latin1', 255, lambda l, c: l * c),
    'VARCHAR': ('utf8', 255, lambda l, c: (l * c) + 1 if l < 256 else (l * c) + 2),
    'VARBINARY': ('utf8', 255, lambda l, c: (l * c) + 1 if l < 256 else (l * c) + 2),
    'TINYBLOB': ('latin1', 2 ** 8, lambda l, c: (l * c) + 1),
    'TINYTEXT': ('utf8', 2 ** 8, lambda l, c: (l * c) + 1),
    'BLOB': ('latin1', 2 ** 16, lambda l, c: (l * c) + 2),
    'TEXT': ('utf8', 2 ** 16, lambda l, c: (l * c) + 2),
    'MEDIUMBLOB': ('latin1', 2 ** 24, lambda l, c: (l * c) + 3),
    'MEDIUMTEXT': ('utf8', 2 ** 32, lambda l, c: (l * c) + 4),
    'LONGBLOB': ('latin1', 2 ** 32, lambda l, c: (l * c) + 4),
    'LONGTEXT': ('utf8', 2 ** 24, lambda l, c: (l * c) + 3),
    'ENUM': ('latin1', 2 ** 8, lambda l, _c: 1 if l <= 2 ** 8 else 2),
    'SET': ('latin1', 4, lambda l, _c: int(math.log(l, 2)))
}

# formula(length) -> size
NUMERIC_TYPES = {
    'BIT': lambda l: int((l + 7) / 8),
    'TINYINT': lambda _l: 1,
    'SMALLINT': lambda _l: 2,
    'MEDIUMINT': lambda _l: 3,
    'INT': lambda _l: 4,
    'INTEGER': lambda _l: 4,
    'BIGINT': lambda _l: 8,
    'DOUBLE': lambda _l: 8,
    'REAL': lambda _l: 8,
    'FLOAT': lambda l: 4 if (l <= 24) else 8,
    'DECIMAL': lambda _l: 4,  # TODO:fix decimal formula
}

# formula(length) -> size
DATE_TYPES = {
    'DATE': 3,
    'TIME': 3,
    'DATETIME': 8,
    'TIMESTAMP': 4,
    'YEAR': 1,
}