import platform

if platform.python_version() < '2.7':
    unittest = __import__('unittest2')
else:
    import unittest

from mse.parser import Parser
from mse.base import Column, Index


class TestParser(unittest.TestCase):
    def setUp(self):
        self.p = Parser()

    def test_parse_index(self):
        i1 = self.p.parse_index("PRIMARY KEY (`runno`)")
        self.assertEquals("primary", i1.name)
        self.assertTrue(i1.is_primary)
        self.assertTrue(i1.is_unique)
        self.assertSequenceEqual(["runno"], i1.columns)
        self.assertEquals(i1, Index("primary", ["runno"], is_unique=True, is_primary=True))

        i2 = self.p.parse_index("KEY idx_Name (name),")
        self.assertEquals("idx_Name", i2.name)
        self.assertFalse(i2.is_primary)
        self.assertFalse(i2.is_unique)
        self.assertSequenceEqual(["name"], i2.columns)

        i3 = self.p.parse_index("unique Key idx_3 (name, id, `a1`),")
        self.assertEquals("idx_3", i3.name)
        self.assertFalse(i3.is_primary)
        self.assertTrue(i3.is_unique)
        self.assertSequenceEqual(["name", "id", "a1"], i3.columns)

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
        self.assertSequenceEqual([Column("id", "int")], t1.columns.values())
        self.assertEquals("INNODB", t1.engine)
        self.assertEquals("utf8", t1.charset)
        self.assertEquals("utf8_general_ci", t1.collation)

        t2 = self.p.parse_table(
            "create table `test`.`t2` (`id` INT NOT NULL DEFAULT 0, PRIMARY KEY (`id`)) collate utf8_general_ci ENGINE=\"MyISAM\"")
        self.assertEquals("t2", t2.name)
        self.assertSequenceEqual([Column("id", "int", nullable=False)], t2.columns.values())
        self.assertSequenceEqual([Index("primary", ['id'], is_primary=True, is_unique=True)], t2.indexes.values())
        self.assertEquals("MyISAM", t2.engine)
        self.assertEquals("utf8", t2.charset)
        self.assertEquals("utf8_general_ci", t2.collation)
