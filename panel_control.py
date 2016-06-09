#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhang 4/5/2016 2:44 PM

"""
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

panel_4 = ModbusClient('192.168.0.104')

value = 1

from time import sleep

while True:
    sleep(1)
    value += 1
    panel_4.write_register(100, value, unit=1)
