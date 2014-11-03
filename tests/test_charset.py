import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

from mse.charset import get_charset, get_collation, fix_charset_collation


class TestCharset(unittest.TestCase):
    def test_get_charset(self):
        charset2 = get_charset('bla')
        self.assertIsNone(charset2)

        charset1 = get_charset('utf8')
        self.assertIsNotNone(charset1)

    def test_get_collation(self):
        collation1 = get_collation("aasd")
        self.assertIsNone(collation1)

        collation2 = get_collation("utf32_icelandic_ci")
        self.assertIsNotNone(collation2)

    def test_fix_charset_collation(self):
        # fails
        self.assertRaises(ValueError, fix_charset_collation, "abc", None)
        self.assertRaises(ValueError, fix_charset_collation, None, "abc")
        self.assertRaises(ValueError, fix_charset_collation, "utf8", "abc")
        self.assertRaises(ValueError, fix_charset_collation, "abc", "utf8_general_ci")
        self.assertRaises(ValueError, fix_charset_collation, "latin1", "utf8_general_ci")

        self.assertSequenceEqual([None, None], fix_charset_collation(None, None))
        self.assertSequenceEqual(["utf8", "utf8_general_ci"], fix_charset_collation("UTF8", None))
        self.assertSequenceEqual(["utf8", "utf8_general_ci"], fix_charset_collation(None, "utf8_GENERAL_ci"))
        self.assertSequenceEqual(["utf8", "utf8_general_ci"], fix_charset_collation("utf8", "utf8_GENERAL_ci"))


