from mse.constants import *
from mse.util import pp_byte, get_effective_charset


class Table:
    def __init__(self, name, engine=None, charset=None):
        self.name = name
        self.columns = {}
        self.indexes = {}
        self.engine = engine
        self.charset = None

        if charset:
            self.charset = get_effective_charset(charset)

    def add_or_update_column(self, column):
        assert isinstance(column, Column)
        self.columns[column.name] = column

    def add_or_update_index(self, index):
        assert isinstance(index, Index)
        for column_name in index.columns:
            if not self.columns.get(column_name):
                raise ValueError(
                    "unable to create index [{}], column [{}] does not exists in table".format(index, column_name))
        self.indexes[index.name] = index


class Index:
    def __init__(self, name, columns, is_primary=False):
        self.name = name
        self.columns = columns
        self.is_primary = is_primary

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        cols = ",".join(self.columns)
        if self.is_primary:
            return "PRIMARY KEY ({0})".format(cols)
        else:
            return "KEY {0} ({1})".format(self.name, cols)


class Column:
    def __init__(self, name, data_type, length=0, decimal=0, nullable=False, charset=None):
        self.name = name
        self.data_type = data_type
        self.length = length
        self.decimal = decimal
        self.nullable = nullable
        self.charset = None

        if charset and (self.data_type in STRING_TYPES):
            self.charset = get_effective_charset(charset)

    def get_size(self):
        if self.data_type in DATE_TYPES:
            return DATE_TYPES[self.data_type]
        elif self.data_type in NUMERIC_TYPES:
            return NUMERIC_TYPES[self.data_type](self.length)
        elif self.data_type in STRING_TYPES:
            (default_charset, default_length, formula) = STRING_TYPES[self.data_type]
            charset = self.charset or default_charset
            length = self.length or default_length
            return formula(CHARSET_SIZE_PER_CHAR[charset], length)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        nn = "" if self.nullable else "NOT NULL"
        charset = "CHARACTER SET {0}".format(self.charset) if self.charset else ""
        if self.decimal > 0:
            return "{0} {1}({2},{3}) {4}".format(self.name, self.data_type, self.length, self.decimal, nn)
        elif self.data_type in DATE_TYPES or self.data_type in NUMERIC_TYPES:
            return "{0} {1} {2}".format(self.name, self.data_type, nn)
        elif self.data_type in STRING_TYPES:
            return "{0} {1}({2}) {3} {4}".format(self.name, self.data_type, self.length, charset, nn)
