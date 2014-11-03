from mse.constants import *
from mse.charset import fix_charset_collation


class EqualityMixin:
    def __eq__(self, other):
        return (type(other) is type(self)) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


class Table(EqualityMixin):
    def __init__(self, name, engine=None, charset=None, collation=None):
        self.name = name
        self.columns = {}
        self.indexes = {}
        self.engine = engine
        self.charset, self.collation = fix_charset_collation(charset, collation)

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


class Index(EqualityMixin):
    def __init__(self, name, columns, is_primary=False, is_unique=False):
        name = name.strip()
        assert name
        assert isinstance(columns, list)
        assert len(columns) >= 1
        self.name = name
        self.columns = columns
        self.is_primary = is_primary
        self.is_unique = is_unique

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        cols = ",".join(self.columns)
        if self.is_primary:
            return "PRIMARY KEY ({0})".format(cols)
        else:
            return "KEY {0} ({1})".format(self.name, cols)


class Column(EqualityMixin):
    def __init__(self, name, data_type, length=0, decimal=None, nullable=True, charset=None, collation=None):
        name = name.strip()
        data_type = data_type.strip().upper()

        assert name
        assert data_type in STRING_TYPES or data_type in NUMERIC_TYPES or data_type in DATE_TYPES

        self.name = name
        self.data_type = data_type
        self.length = length
        self.decimal = decimal
        self.nullable = nullable
        self.charset, self.collation = fix_charset_collation(charset, collation)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        nn = "" if self.nullable else "NOT NULL"

        if self.decimal is not None:
            return "{0} {1}({2},{3}) {4}".format(self.name, self.data_type, self.length, self.decimal, nn)
        elif self.data_type in DATE_TYPES or self.data_type in NUMERIC_TYPES:
            return "{0} {1} {2}".format(self.name, self.data_type, nn)
        elif self.data_type in STRING_TYPES:
            charset_string = "CHARACTER SET {0} COLLATION {1}".format(self.charset,
                                                                      self.collation) if self.charset else ""
            return "{0} {1}({2}) {3} {4}".format(self.name, self.data_type, self.length, charset_string, nn)
