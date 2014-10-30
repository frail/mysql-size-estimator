# -*- coding: utf-8 -*-
"""
================================
Util
================================

Some utility stuff
"""

import math
from mse.constants import CHARSET_SIZE_PER_CHAR


def get_effective_charset(charset):
    """
    get effective charset without collation
    """
    c = charset.lower()
    for charset_name in CHARSET_SIZE_PER_CHAR.keys():
        if c.startswith(charset_name):
            return charset_name
    raise ValueError("unknown charset : {}".format(charset))


def pp_byte(byte):
    """
    pretty prints byte value
    """
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    if byte > 0:
        i = min(int(math.floor(math.log(byte, 1024))), len(size_name) - 1)
        p = math.pow(1024, i)
        s = round(byte / p, 2)
        return '%s %s' % (s, size_name[i])
    else:
        return '0B'


def pp_num(num):
    """
    pretty prints number
    """
    if num > 0:
        size_name = ("", "K", "M", "T")
        i = min(int(math.floor(math.log(num, 1000))), len(size_name) - 1)
        p = math.pow(1000, i)
        s = round(num / p, 2)
        return '%s %s' % (s, size_name[i])
    else:
        return "%s" % num

