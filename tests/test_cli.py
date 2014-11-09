import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

import mse
from mse.cli import Cli, CliSQLParseException
from docopt import docopt, DocoptExit


class TestCli(unittest.TestCase):

    def test_fail_no_param(self):
        self.assertRaises(DocoptExit, docopt, mse.cli.__doc__)

    def test_fail_simple_selection(self):
        self.assertRaises(DocoptExit, docopt, mse.cli.__doc__, ['dummy'])
        self.assertRaises(DocoptExit, docopt, mse.cli.__doc__, ['file'])

    def test_dummy(self):
        args = docopt(mse.cli.__doc__, ['dummy', '-c', 'id INT'])
        parsed = Cli(args)
        self.assertEqual("dummy", parsed.table.name)
        self.assertEqual(1, len(parsed.table.columns))
        self.assertEqual(0, len(parsed.table.indexes))

    def test_dummy_fail_bad_definition(self):
        args1 = docopt(mse.cli.__doc__, ['dummy', '-c', 'id'])
        self.assertRaises(CliSQLParseException, Cli, args1)

        args2 = docopt(mse.cli.__doc__, ['dummy', '-c','id INT', '-i', 'id'])
        self.assertRaises(CliSQLParseException, Cli, args2)



