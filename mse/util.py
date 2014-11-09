# -*- coding: utf-8 -*-
"""
================================
Util
================================

Some utility stuff
"""

import math

BYTE_SUFFIXES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def pp_byte(nbytes):
    """
    pretty prints byte value
    """
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(BYTE_SUFFIXES)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, BYTE_SUFFIXES[i])


def strip_quotes(s):
    if s and len(s) >= 2 and s[0] == s[-1] and s[0] in ["\"", "'", "`"]:
        return s[1:-1]
    return s


def to_str_list(stuff):
    """
    return given parameter as a list of string
    """
    if isinstance(stuff, str):
        return [stuff]
    try:
        _iterator = iter(stuff)
    except TypeError:
        return [str(stuff)]
    else:
        return [str(x) for x in stuff]


def pp_num(num):
    """
    pretty prints number with commas
    """
    s = '%d' % num
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))

