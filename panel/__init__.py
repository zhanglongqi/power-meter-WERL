#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 29/Jan/16 15:24

"""
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from ac_meter import SchneiderPM710, MeterData
from utils import FloatData
from time import time


class Panel:
    def __init__(self, ip):
        self.client = ModbusClient(ip)

        self.AC_Meter_0 = SchneiderPM710(unit_id=2)
        self.AC_Meter_1 = SchneiderPM710(unit_id=3)

    def read_and_parse_from_ModbusTCP(self):
        for i in range(0, 2):

            data = MeterData()
            data['time'] = time()

            if i == 0:
                res = self.client.read_holding_registers(999, 22, unit=self.AC_Meter_0.unit_id)
            elif i == 1:
                res = self.client.read_holding_registers(999, 22, unit=self.AC_Meter_1.unit_id)

            real_energy = FloatData()
            real_energy.shorts.s0 = res.registers[1]
            real_energy.shorts.s1 = res.registers[0]
            data['real_energy'] = real_energy.float

            real_power = FloatData()
            real_power.shorts.s0 = res.registers[7]
            real_power.shorts.s1 = res.registers[6]
            data['real_power'] = real_power.float

            reactive_power = FloatData()
            reactive_power.shorts.s0 = res.registers[11]
            reactive_power.shorts.s1 = res.registers[10]
            data['reactive_power'] = reactive_power.float

            voltage_LL = FloatData()
            voltage_LL.shorts.s0 = res.registers[15]
            voltage_LL.shorts.s1 = res.registers[14]
            data['voltage_LL'] = voltage_LL.float

            frequency = FloatData()
            frequency.shorts.s0 = res.registers[21]
            frequency.shorts.s1 = res.registers[20]
            data['frequency'] = frequency.float

            if i == 0:
                self.AC_Meter_0.data.append(data)
            elif i == 1:
                self.AC_Meter_1.data.append(data)
