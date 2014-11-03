# -*- coding: utf-8 -*-
import pyparsing as p
from mse.constants import STRING_TYPES, NUMERIC_TYPES, DATE_TYPES
from mse.base import Column, Index, Table
from mse.util import to_str_list, strip_quotes as sq

DATA_TYPE_LITERALS = list(STRING_TYPES) + list(NUMERIC_TYPES) + list(DATE_TYPES)


class Parser:
    _quoted = p.dblQuotedString | p.sglQuotedString
    _name = p.Word(p.alphas + "_", p.alphanums + "_") | p.QuotedString("`")
    _nums = p.Word(p.nums)
    _any = _name | _quoted | _nums

    # not null / charset meta information
    _nn = (p.CaselessLiteral("NOT") + p.CaselessLiteral("NULL")).setResultsName("not_null")
    _cs = p.Optional(p.CaselessLiteral("DEFAULT")) + p.CaselessLiteral("CHARACTER") + p.CaselessLiteral("SET") + \
          p.Optional("=") + _any.setResultsName("charset")
    _co = p.Optional(p.CaselessLiteral("DEFAULT")) + p.CaselessLiteral("COLLATE") + p.Optional("=") + \
          _any.setResultsName("collate")
    _en = p.CaselessLiteral("ENGINE") + p.Optional("=") + _any.setResultsName("engine")

    # column data type and length
    _column_data_type = \
        p.oneOf(DATA_TYPE_LITERALS, caseless=True).setResultsName("type") + \
        p.Optional("(" + _nums.setResultsName("length") + ")") + \
        p.Optional("(" + p.delimitedList(_quoted).setResultsName("enum_set_values") + ")") + \
        p.Optional("(" + _nums.setResultsName("length") + "," + _nums.setResultsName("decimal") + ")")

    _column_definition = \
        _name.setResultsName("name") + _column_data_type + p.Optional(p.OneOrMore(_nn | _cs | _co | _any))

    # index definition
    _index_definition = \
        p.Optional(p.CaselessLiteral("PRIMARY").setResultsName("is_primary")) + \
        p.Optional(p.CaselessLiteral("UNIQUE").setResultsName("is_unique")) + \
        p.CaselessLiteral("KEY") + p.Optional(_name.setResultsName("name")) + "(" + \
        p.delimitedList(_name).setResultsName("columns") + ")"

    # table definition
    _table_definition = \
        p.CaselessLiteral("CREATE") + p.CaselessLiteral("TABLE") + \
        p.Optional(_name.setResultsName("database_name") + ".") + \
        _name.setResultsName("table_name") + \
        "(" + p.delimitedList(_column_definition | _index_definition) + ")" + \
        p.Optional(p.OneOrMore(_cs | _co | _en | _any))

    def _on_column_parse(self, tokens):
        length = len(tokens.get("enum_set_values", [])) if tokens.get("enum_set_values") else int(
            tokens.get("length", 0))
        decimal = int(tokens.get("decimal")) if tokens.get("decimal") else None
        charset = sq(tokens.get("charset"))
        collation = sq(tokens.get("collate"))
        nullable = tokens.get("not_null") is None
        column = Column(tokens["name"], tokens["type"], length=length, decimal=decimal, nullable=nullable,
                        charset=charset, collation=collation)
        self.columns.append(column)

    def _on_index_parse(self, tokens):
        is_primary = tokens.get("is_primary") is not None
        columns = to_str_list(tokens.get("columns"))

        if is_primary:
            name = 'primary'
            is_unique = True
        else:
            name = tokens.get("name")
            is_unique = tokens.get("is_unique") is not None

        index = Index(name, columns, is_primary, is_unique)
        self.indexes.append(index)

    def _on_table_parse(self, tokens):
        self.table_name = tokens.get("table_name")
        self.table_collation = sq(tokens.get("collate"))
        self.table_charset = sq(tokens.get("charset"))
        self.table_engine = sq(tokens.get("engine"))

    def _reset(self):
        self.table_name = None
        self.table_engine = None
        self.table_charset = None
        self.table_collation = None
        self.columns = []
        self.indexes = []

    def __init__(self):
        self._reset()
        self._column_definition.setParseAction(self._on_column_parse)
        self._index_definition.setParseAction(self._on_index_parse)
        self._table_definition.setParseAction(self._on_table_parse)

    def parse_table(self, s):
        self._reset()
        self._table_definition.parseString(s)
        table = Table(self.table_name, engine=self.table_engine, charset=self.table_charset,
                      collation=self.table_collation)

        for column in self.columns:
            table.add_or_update_column(column)

        for index in self.indexes:
            table.add_or_update_index(index)

        return table

    def parse_index(self, s):
        self._reset()
        self._index_definition.parseString(s)
        return self.indexes[0]

    def parse_column(self, s):
        self._reset()
        self._column_definition.parseString(s)
        return self.columns[0]