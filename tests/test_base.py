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

    def test_add_index_to_unknown_column(self):
        self.assertRaises(ValueError, self.table.add_or_update_index, Index("test", ['unknown_column']))


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

    def test_to_string(self):
        c1 = Column("id", "int")
        c2 = Column("name", "varchar", length=30, nullable=False, collation="utf8_general_ci")
        c3 = Column("price", "DECIMAL", length=8, decimal=2)

        self.assertEqual("id INT", str(c1))
        self.assertEqual("name VARCHAR(30) CHARACTER SET utf8 COLLATION utf8_general_ci NOT NULL", str(c2))
        self.assertEqual("price DECIMAL(8,2)", str(c3))

        self.assertEqual("[id INT, price DECIMAL(8,2)]", str([c1,c3]))


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

    def test_to_string(self):
        i1 = Index("primary", ['id'], is_primary=True)
        i2 = Index("idx_1", ['a', 'b'], is_primary=False, is_unique=False)
        i3 = Index("idx_2", ['b'], is_primary=False, is_unique=True)
        self.assertEqual("PRIMARY KEY (id)", str(i1))
        self.assertEqual("KEY idx_1 (a,b)", str(i2))
        self.assertEqual("UNIQUE KEY idx_2 (b)", str(i3))
        self.assertEqual("[PRIMARY KEY (id), UNIQUE KEY idx_2 (b)]", str([i1,i3]))



