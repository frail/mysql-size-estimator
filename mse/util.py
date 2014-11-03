# -*- coding: utf-8 -*-
"""
================================
Util
================================

Some utility stuff
"""

import math


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


def strip_quotes(s):
    if s and len(s) >= 2 and s[0] == s[-1] and s[0] in ["\"", "'", "`"]:
        return s[1:-1]
    return s


def to_str_list(stuff):
    """
    return given parameter as a list of string
    """
    try:
        _iterator = iter(stuff)
    except TypeError:
        return [str(stuff)]
    else:
        return [str(x) for x in stuff]


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

