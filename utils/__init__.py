#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 29/Jan/16 16:01

"""
from ctypes import *


class Data_Char4(Structure):
    _fields_ = [("c0", c_uint8, 8),
                ("c1", c_uint8, 8),
                ("c2", c_uint8, 8),
                ("c3", c_uint8, 8)]


class Data_Short2(Structure):
    _fields_ = [("s0", c_uint16, 16),
                ("s1", c_uint16, 16),
                ]


class FloatData(Union):
    _fields_ = [
        ("float", c_float),
        ("chars", Data_Char4),
        ("shorts", Data_Short2)
    ]
