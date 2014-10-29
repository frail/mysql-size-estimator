import math
from mse.base import Table
from mse.util import pp_byte, pp_num

INNODB_STORAGE_EXTRAS = [
    ('INNODB ROW HEADER', 5),
    ('INNODB TRX_ID', 6),
    ('INNODB ROLL_PTR', 7),
]

INNODB_MIN_PAGE_FILL_RATE = 0.07
INNODB_MAX_PAGE_FILL_RATE = 0.50

DEFAULT_ROW_SIZES = [
    10 ** 6,
    5 * (10 ** 6),
    10 ** 7,
    5 * (10 ** 7),
    10 ** 8
]


class InnoDBEstimator:
    """
    Estimator for innodb
    """
    LINE_BREAK = "=" * 60

    def __init__(self, table):
        assert isinstance(table, Table)
        self.table = table

        # do calculations
        self.row_data_size, d_1 = self.get_row_data_size()
        self.row_index_size, d_2 = self.get_row_index_size()
        self.row_null_bitmap_size, d_3 = self.get_row_null_bitmap_size()
        self.row_overhead_size, d_4 = self.get_row_overhead_size()

        self.row_total_size = self.row_data_size + self.row_index_size + self.row_null_bitmap_size + \
                              self.row_overhead_size

        self.details = d_1 + d_2 + d_3 + d_4

    def estimate(self, row_counts, print_details=True):
        print "Estimations for table : [{}] ".format(self.table.name)

        # if row sizes is not specified, use defaults
        if not row_counts or len(row_counts) == 0:
            row_counts = DEFAULT_ROW_SIZES
        # print details
        if print_details:
            print self.LINE_BREAK
            # create some more details
            d_p = self.row_data_size * 100 / self.row_total_size
            i_p = self.row_index_size * 100 / self.row_total_size
            o_p = (self.row_null_bitmap_size + self.row_overhead_size) * 100 / self.row_total_size
            self.details.append(
                "[PERCENTAGES] data : {0:.2f}% | index : {1:.2f}% | other : {2:.2f}".format(d_p, i_p, o_p))

            # print them out
            for detail in self.details:
                print detail

            print self.LINE_BREAK

        estimate_table_template = "{0: <15}  |  {1: <20}  |  {2: <20}  |  {3: <20}"

        print estimate_table_template.format("ROWS", "NO FRAGMENTATION", "MIN FRAGMENTATION", "MAX FRAGMENTATION")
        for rows in row_counts:
            t = self.row_total_size
            print estimate_table_template.format(
                pp_num(rows), pp_byte(t * rows),
                pp_byte(t * (1 + INNODB_MIN_PAGE_FILL_RATE) * rows),
                pp_byte(t * (1 + INNODB_MAX_PAGE_FILL_RATE) * rows),
            )

    # note : does not add primary index size !
    def _calculate_index_size(self, index):
        total = 0
        for column_name in index.columns:
            total += self.table.columns.get(column_name).get_size()
        return total

    def get_row_data_size(self):
        details = []
        total = 0.0
        for column in self.table.columns.values():
            size = column.get_size()
            details.append("[COLUMN] {} [{}]".format(column, pp_byte(size)))
            total += column.get_size()
        return total, details

    def get_row_index_size(self):
        details = []
        total = 0
        primary_index = self.table.indexes.get("primary")

        if not primary_index:
            primary_index_size = 6
            details.append("[INDEX] fake primary index [{}]".format(pp_byte(primary_index_size)))
        else:
            primary_index_size = self._calculate_index_size(primary_index)
            details.append("[INDEX] {} [{}]".format(primary_index, pp_byte(primary_index_size)))

        total += primary_index_size

        for index in self.table.indexes.values():
            if index.is_primary:
                continue
            secondary_index_size = self._calculate_index_size(index)
            secondary_index_size += primary_index_size
            details.append("[INDEX] {} [{}]".format(index, pp_byte(secondary_index_size)))
            total += secondary_index_size

        return total, details

    def get_row_overhead_size(self):
        details = []
        total = 0
        for (extra, b) in INNODB_STORAGE_EXTRAS:
            details.append("[INNODB-OVERHEAD] {} [{}]".format(extra, pp_byte(b)))
            total += b
        return total, details

    def get_row_null_bitmap_size(self):
        details = []
        nullable_column_count = 0
        for column in self.table.columns.values():
            if column.nullable:
                nullable_column_count += 1
        total = int(math.ceil((7 + nullable_column_count) / 8.0))
        details.append("[NULL-BITMAP] {} null columns [{}]".format(nullable_column_count, pp_byte(total)))
        return total, details



