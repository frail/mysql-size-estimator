import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

import mse
from mse.base import Column, Index, IndexColumn
from mse.cli import Cli, CliSQLParseException
from docopt import docopt, DocoptExit


class TestCli(unittest.TestCase):
    def test_fail_no_param(self):
        self.assertRaises(DocoptExit, docopt, mse.cli.__doc__)

    def test_fail_simple_selection(self):
        self.assertRaises(DocoptExit, docopt, mse.cli.__doc__, ['dummy'])
        self.assertRaises(DocoptExit, docopt, mse.cli.__doc__, ['file'])

    def test_dummy(self):
        args = docopt(mse.cli.__doc__, ['dummy', '-c', 'id INT', '-i', 'PRIMARY KEY (id)'])
        parsed = Cli(args)
        self.assertEqual("dummy", parsed.table.name)
        self.assertEqual(Column('id', 'INT'), parsed.table.columns.get('id'))
        self.assertEqual(Index('primary', [IndexColumn('id')], is_primary=True), parsed.table.indexes.get('primary'))

    def test_dummy_fail_bad_definition(self):
        args1 = docopt(mse.cli.__doc__, ['dummy', '-c', 'id'])
        self.assertRaises(CliSQLParseException, Cli, args1)

        args2 = docopt(mse.cli.__doc__, ['dummy', '-c', 'id INT', '-i', 'id'])
        self.assertRaises(CliSQLParseException, Cli, args2)



