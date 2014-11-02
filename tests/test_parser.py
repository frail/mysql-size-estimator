from unittest import TestCase
from mse.parser import Parser


class TestParser(TestCase):
    def setUp(self):
        self.p = Parser()

    def test_parse_index(self):
        i1 = self.p.parse_index("PRIMARY KEY (`runno`)")
        self.assertEquals("primary", i1.name)
        self.assertTrue(i1.is_primary)
        self.assertTrue(i1.is_unique)
        self.assertItemsEqual(["runno"], i1.columns)

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
        c1 = self.p.parse_column("data VARCHAR(100)")


    def test_parse_table(self):
        pass