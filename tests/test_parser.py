import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

from mse.parser import Parser
from mse.base import Column, Index, IndexColumn


class TestParser(unittest.TestCase):
    def setUp(self):
        self.p = Parser()

    def test_parse_index_1(self):
        i1 = self.p.parse_index("PRIMARY KEY (`runno`)")
        self.assertEquals("primary", i1.name)
        self.assertTrue(i1.is_primary)
        self.assertTrue(i1.is_unique)
        self.assertSequenceEqual("runno", i1.columns[0].name)
        self.assertEquals(i1, Index("primary", [IndexColumn("runno")], is_unique=True, is_primary=True))

    def test_parse_index_2(self):
        i2 = self.p.parse_index("KEY idx_Name (name(10) DESC, other_key),")
        self.assertEquals("idx_Name", i2.name)
        self.assertFalse(i2.is_primary)
        self.assertFalse(i2.is_unique)
        self.assertSequenceEqual([IndexColumn("name", 10, "DESC"), IndexColumn("other_key")], i2.columns)


    def test_parse_index_3(self):
        i3 = self.p.parse_index("unique Key idx_3 (name, id, `a1`),")
        self.assertEquals("idx_3", i3.name)
        self.assertFalse(i3.is_primary)
        self.assertTrue(i3.is_unique)
        self.assertSequenceEqual([IndexColumn("name"), IndexColumn("id"), IndexColumn("a1")], i3.columns)

    def test_parse_index_4(self):
        i4 = self.p.parse_index("index idx_Name (name),")
        self.assertEquals("idx_Name", i4.name)
        self.assertFalse(i4.is_primary)
        self.assertFalse(i4.is_unique)
        self.assertSequenceEqual([IndexColumn("name")], i4.columns)

    def test_parse_column(self):
        c1 = self.p.parse_column("id int")
        self.assertEquals(c1, Column("id", "INT"))

        c2 = self.p.parse_column("`f2` Decimal(10,1) NOT NULL DEFAULT '0.2'")
        self.assertEquals(c2, Column("f2", "DECIMAL", length=10, decimal=1, nullable=False))

        c3 = self.p.parse_column("f3 VARCHAR")
        self.assertEquals(c3, Column("f3", "VARCHAR", length=0))

    def test_parse_table(self):
        t1 = self.p.parse_table("create table test.t1 (id INT) engine=INNODB CHARACTER SET 'UTF8'")
        self.assertEquals("t1", t1.name)
        self.assertSequenceEqual([Column("id", "int")], list(t1.columns.values()))
        self.assertEquals("INNODB", t1.engine)
        self.assertEquals("utf8", t1.charset)
        self.assertEquals("utf8_general_ci", t1.collation)

        t2 = self.p.parse_table(
            "create table `test`.`t2` (`id` INT NOT NULL DEFAULT 0, PRIMARY KEY (`id`)) collate utf8_general_ci ENGINE=\"MyISAM\"")
        self.assertEquals("t2", t2.name)
        self.assertSequenceEqual([Column("id", "int", nullable=False)], list(t2.columns.values()))
        self.assertSequenceEqual([Index("primary", [IndexColumn('id')], is_primary=True, is_unique=True)], list(t2.indexes.values()))
        self.assertEquals("MyISAM", t2.engine)
        self.assertEquals("utf8", t2.charset)
        self.assertEquals("utf8_general_ci", t2.collation)
