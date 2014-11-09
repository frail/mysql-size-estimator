import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

import mse
from docopt import docopt, DocoptExit


class TestCli(unittest.TestCase):
    def test_fail_no_param(self):
        self.assertRaises(DocoptExit, docopt, mse.cli.__doc__)


