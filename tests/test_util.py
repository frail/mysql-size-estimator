import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

from mse.util import *


class TestUtil(unittest.TestCase):

    def test_pp_byte(self):
        self.assertEqual("0 B", pp_byte(0))
        self.assertEqual("1 KB", pp_byte(1024))
        self.assertEqual("1.01 KB", pp_byte(1030))
        self.assertEqual("1.99 MB", pp_byte(2*(1024*1019)))

    def test_strip_quotes(self):
        self.assertEqual("a", strip_quotes("\"a\""))
        self.assertEqual("a", strip_quotes("'a'"))
        self.assertEqual("a", strip_quotes("`a`"))
        self.assertEqual("a'b'c", strip_quotes("'a'b'c'"))
        self.assertEqual("\"a", strip_quotes("\"a"))

    def test_to_str_list(self):
        self.assertSequenceEqual(['abc'], to_str_list('abc'))
        self.assertSequenceEqual(['1', '2'], to_str_list([1, 2]))
        self.assertSequenceEqual(['123'], to_str_list(123))
        self.assertSequenceEqual(['1', '2'], to_str_list(['1', '2']))

    def test_pp_num(self):
        self.assertEqual("1,000", pp_num(1000))
        self.assertEqual("2,134,024", pp_num(2134024))
