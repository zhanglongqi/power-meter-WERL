#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 29/Jan/16 15:30

"""
from collections import UserDict


class MeterData(UserDict):
    def __init__(self):
        self.data = {
            'time': 0,
            'real_energy': 0,
            'real_energy': 0,
            'real_power': 0,
            'reactive_power': 0,
            'voltage_LL': 0,
            'frequency': 0
        }


class SchneiderPM710:
    def __init__(self, unit_id):
        self.unit_id = unit_id
        self.data = []
