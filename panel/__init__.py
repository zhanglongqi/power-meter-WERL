#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 29/Jan/16 15:24

"""
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from time import time, strftime
from logging import getLogger
from random import random
from openpyxl import Workbook

from ac_meter import SchneiderPM710, MeterData
from utils import FloatData
from main import debug


class Panel():
    def __init__(self, ip, name):
        self.client = ModbusClient(ip)

        self.AC_Meter_0 = SchneiderPM710(unit_id=2)
        self.AC_Meter_1 = SchneiderPM710(unit_id=3)

        self.name = name
        self.logger = getLogger(self.name)

        self.book = Workbook()

        self.sheet_for_AC_Meter_0 = self.book.active
        self.sheet_for_AC_Meter_0.title = 'AC_Meter_0'

        self.sheet_for_AC_Meter_1 = self.book.active
        self.sheet_for_AC_Meter_1.title = 'AC_Meter_1'

    def read_and_parse_from_ModbusTCP(self):
        for i in range(0, 2):

            data = MeterData()
            data['time'] = time()

            if i == 0:
                res = self.client.read_holding_registers(999, 22, unit=self.AC_Meter_0.unit_id) if not debug else None
            elif i == 1:
                res = self.client.read_holding_registers(999, 22, unit=self.AC_Meter_1.unit_id) if not debug else None

            real_energy = FloatData()
            real_energy.shorts.s0 = res.registers[1] if not debug else random() * 100
            real_energy.shorts.s1 = res.registers[0] if not debug else random() * 100
            data['real_energy'] = real_energy.float

            real_power = FloatData()
            real_power.shorts.s0 = res.registers[7] if not debug else random() * 100
            real_power.shorts.s1 = res.registers[6] if not debug else random() * 100
            data['real_power'] = real_power.float

            reactive_power = FloatData()
            reactive_power.shorts.s0 = res.registers[11] if not debug else random() * 100
            reactive_power.shorts.s1 = res.registers[10] if not debug else random() * 100
            data['reactive_power'] = reactive_power.float

            voltage_LL = FloatData()
            voltage_LL.shorts.s0 = res.registers[15] if not debug else random() * 100
            voltage_LL.shorts.s1 = res.registers[14] if not debug else random() * 100
            data['voltage_LL'] = voltage_LL.float

            frequency = FloatData()
            frequency.shorts.s0 = res.registers[21] if not debug else random() * 100
            frequency.shorts.s1 = res.registers[20] if not debug else random() * 100
            data['frequency'] = frequency.float

            if i == 0:
                self.AC_Meter_0.data.append(data)
            elif i == 1:
                self.AC_Meter_1.data.append(data)

            self.logger.info(data)

    def save_data(self):
        self.sheet_for_AC_Meter_0.append(
            ('time', 'real_energy', 'real_power', 'reactive_power', 'voltage_LL', 'frequency'))
        for row in range(start=1, stop=len(self.AC_Meter_0.data)):
            self.sheet_for_AC_Meter_0.append((
                strftime('%H:%M:%S %d-%b-%Y', self.AC_Meter_0.data['time']),
                self.AC_Meter_0.data['real_energy'],
                self.AC_Meter_0.data['real_power'],
                self.AC_Meter_0.data['reactive_power'],
                self.AC_Meter_0.data['voltage_LL'],
                self.AC_Meter_0.data['frequency']))

        self.book.save(filename=self.name + '-' + strftime('%H:%M:%S %d-%b-%Y') + '.xlsx')
