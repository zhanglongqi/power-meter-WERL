#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 29/Jan/16 13:48

# 1000 float Real Energy, Consumption
# 1006 float Real Power, Total
# 1010 float Reactive Power, Total
# 1014 float Voltage, L-L, 3P Average
# 1020 float Frequency

read data from AC power meter Schneider PM710 and save
"""

from pymodbus.client.sync import ModbusTcpClient
from utils import FloatData

p1 = ModbusTcpClient('192.168.0.101')

p1_ac1 = p1.read_holding_registers(999, 22, unit=2)
p1_ac2 = p1.read_holding_registers(999, 22, unit=3)

data = {}

real_energy = FloatData()
real_energy.shorts.s0 = p1_ac1.registers[1]
real_energy.shorts.s1 = p1_ac1.registers[0]
data['real_energy'] = real_energy.float

real_power = FloatData()
real_power.shorts.s0 = p1_ac1.registers[7]
real_power.shorts.s1 = p1_ac1.registers[6]
data['real_power'] = real_power.float

reactive_power = FloatData()
reactive_power.shorts.s0 = p1_ac1.registers[11]
reactive_power.shorts.s1 = p1_ac1.registers[10]
data['reactive_power'] = reactive_power.float

voltage_LL = FloatData()
voltage_LL.shorts.s0 = p1_ac1.registers[15]
voltage_LL.shorts.s1 = p1_ac1.registers[14]
data['voltage_LL'] = voltage_LL.float

frequency = FloatData()
frequency.shorts.s0 = p1_ac1.registers[21]
frequency.shorts.s1 = p1_ac1.registers[20]
data['frequency'] = frequency.float

print(data)
