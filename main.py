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
from time import sleep
from panel import Panel


def main():
    p1 = Panel('192.168.1.101', 'P1')
    p2 = Panel('192.168.1.102', 'P2')
    p3 = Panel('192.168.1.103', 'P3')
    p4 = Panel('192.168.1.104', 'P4')
    p5 = Panel('192.168.1.105', 'P5')
    p6 = Panel('192.168.1.106', 'P6')
    p7 = Panel('192.168.1.107', 'P7')
    p8 = Panel('192.168.1.108', 'P8')

    for i in range(0, 10):
        # sleep(1)
        p1.read_and_parse_from_ModbusTCP()
        p2.read_and_parse_from_ModbusTCP()
        p3.read_and_parse_from_ModbusTCP()
        p4.read_and_parse_from_ModbusTCP()
        p5.read_and_parse_from_ModbusTCP()
        p6.read_and_parse_from_ModbusTCP()
        p7.read_and_parse_from_ModbusTCP()
        p8.read_and_parse_from_ModbusTCP()

    p1.save_data()
    p2.save_data()
    p3.save_data()
    p4.save_data()
    p5.save_data()
    p6.save_data()
    p7.save_data()
    p8.save_data()


if __name__ == "__main__":
    print('Author longqi.\n', 'Read data from AC power meter Schneider PM710 in WERL and save\n')
    main()
