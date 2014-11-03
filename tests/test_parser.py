from unittest import TestCase
from mse.parser import Parser
from mse.base import Column,Index


class TestParser(TestCase):
    def setUp(self):
        self.p = Parser()

    def test_parse_index(self):
        i1 = self.p.parse_index("PRIMARY KEY (`runno`)")
        self.assertEquals("primary", i1.name)
        self.assertTrue(i1.is_primary)
        self.assertTrue(i1.is_unique)
        self.assertItemsEqual(["runno"], i1.columns)
        self.assertEquals(i1, Index("primary", ["runno"], is_unique=True, is_primary=True))

        i2 = self.p.parse_index("KEY idx_Name (name),")
        self.assertEquals("idx_Name", i2.name)
        self.assertFalse(i2.is_primary)
        self.assertFalse(i2.is_unique)
        self.assertItemsEqual(["name"], i2.columns)

        i3 = self.p.parse_index("unique Key idx_3 (name, id, `a1`),")
        self.assertEquals("idx_3", i3.name)
        self.assertFalse(i3.is_primary)
        self.assertTrue(i3.is_unique)
        self.assertItemsEqual(["name", "id", "a1"], i3.columns)

    def test_parse_column(self):
        c1 = self.p.parse_column("id int")
        self.assertEquals(c1, Column("id", "INT"))

        c2 = self.p.parse_column("`f2` Decimal(10,1) NOT NULL DEFAULT '0.2'")
        self.assertEquals(c2, Column("f2", "DECIMAL", length=10, decimal=1, nullable=False))



    def test_parse_table(self):
        pass