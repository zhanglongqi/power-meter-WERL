#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 29/Jan/16 13:48

# 1000 float Real Energy, Consumption
# 1006 float Real Power, Total
# 1010 float Reactive Power, Total
# 1014 float Voltage, L-L, 3P Average
# 1020 float Frequency

read data from AC power meter Sch
"""

from pymodbus.client.sync import ModbusTcpClient
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


class Data(Union):
    _fields_ = [
        ("float", c_float),
        ("chars", Data_Char4),
        ("shorts", Data_Short2)
    ]


p1 = ModbusTcpClient('192.168.0.101')
p1_ac1 = p1.read_holding_registers(999, 21, unit=2)
p1_ac2 = p1.read_holding_registers(999, 21, unit=3)

print(p1_ac1.registers)

print(p1_ac2.registers)

real_energy = Data()
real_energy.shorts.s0 = p1_ac1.registers[1]
real_energy.shorts.s1 = p1_ac1.registers[0]

print(real_energy.float)
