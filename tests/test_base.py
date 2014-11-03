import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest
from mse.base import Table, Column, Index


class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table("test1")

    def test_add_column(self):
        c1 = Column("c1", "INT")
        self.table.add_or_update_column(c1)
        self.assertEquals(c1, self.table.columns["c1"])
        self.assertEquals(1, len(self.table.columns))

    def test_update_column(self):
        c1 = Column("c1", "INT")
        self.table.add_or_update_column(c1)
        c1b = Column("c1", "BIGINT")
        self.table.add_or_update_column(c1b)
        self.assertNotEqual(c1, self.table.columns["c1"])
        self.assertEqual(c1b, self.table.columns["c1"])
        self.assertEquals(1, len(self.table.columns))

    def test_multiple_insert_update_column(self):
        for i in range(1, 10):
            self.table.add_or_update_column(Column("e" + str(i), "INT"))

        self.assertEquals(9, len(self.table.columns))
        self.assertEquals("INT", self.table.columns['e7'].data_type)


class TestColumn(unittest.TestCase):
    def test_create_fails(self):
        self.assertRaises(AssertionError, Column, "", "int")
        self.assertRaises(AssertionError, Column, "test", "int2")
        self.assertRaises(AssertionError, Column, "  ", "BIGINT")

    def test_defaults(self):
        c = Column("name", "VarChar")
        self.assertEquals("name", c.name)
        self.assertEquals("VARCHAR", c.data_type)
        self.assertEquals(0, c.length)
        self.assertEquals(None, c.decimal)
        self.assertIsNone(c.charset)
        self.assertIsNone(c.collation)


class TestIndex(unittest.TestCase):
    def test_create_fail(self):
        self.assertRaises(AssertionError, Index, " ", ["a", "b"])
        self.assertRaises(AssertionError, Index, "test", "column")
        self.assertRaises(AssertionError, Index, "test", [])

    def test_defaults(self):
        i = Index("test", ['a', 'b', 'c'])
        self.assertEquals("test", i.name)
        self.assertSequenceEqual(['a', 'b', 'c'], i.columns)
        self.assertEquals(False, i.is_primary)
        self.assertEquals(False, i.is_unique)