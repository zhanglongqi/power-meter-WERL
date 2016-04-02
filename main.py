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
from queue import Queue, Empty
import threading
import signal
import time
import sys, os

message = Queue()


def working():
    p1 = Panel('192.168.0.101', 'P1')
    p2 = Panel('192.168.0.102', 'P2')
    p3 = Panel('192.168.0.103', 'P3')
    p4 = Panel('192.168.0.104', 'P4')
    p5 = Panel('192.168.0.105', 'P5')
    p6 = Panel('192.168.0.106', 'P6')
    p7 = Panel('192.168.0.107', 'P7')
    # p8 = Panel('192.168.0.108', 'P8')
    panels = [p1, p2, p3, p4, p5, p6, p7]

    while True:
        try:
            cmd = message.get_nowait()
            message.task_done()
        except Empty:
            cmd = 'CONTINUE'

        if cmd == 'CONTINUE':
            for panel in panels:
                panel.read_and_parse_from_ModbusTCP()

            print('.', end='', flush=True)
            sleep(1)

        elif cmd == 'SAVE':
            for panel in panels:
                panel.save_data_spreadsheet()
            print(' Done ')

        elif cmd == 'CLEAR':
            for panel in panels:
                panel.clear_data()
            print(' Done ')

        elif cmd == 'QUIT':
            print(' Quit ')
            sys.exit()
            break
        elif cmd == 'NEW':
            for panel in panels:
                panel.save_data_spreadsheet()

            for panel in panels:
                panel.clear_data()

            print(' Done ')


def cli():
    print('''\n
    ****************************************************************************\n
    *****************    Welcome to the AC/DC meter data panel *****************\n
    ****                    <s> (save) to save data                         ****\n
    ****                    <c> (clear) to clear previous data              ****\n
    ****                    <n> (new) to save and start new session         ****\n
    ****                    <q> (quit) to quit the app                      ****\n
    ****************************************************************************\n
        ''')

    getchar = None
    if os.name == 'nt':
        try:
            import termios
        except ImportError:
            # Non-POSIX. Return msvcrt's (Windows') getch.
            import msvcrt
            getchar = msvcrt.getwch
    else:
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys, tty
        def _getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        getchar = _getch

    while True:
        cmd = getchar()
        if cmd == 'q':
            message.put('QUIT')
            sys.exit(0)

        if cmd == 's':
            message.put('SAVE')
            print('Saving current session ...', end='')

        elif cmd == 'c':
            print('Clear current data ...', end='')
            message.put('CLEAR')

        elif cmd == 'n':
            print('Saving current session and start new one ...', end='')
            message.put('NEW')


if __name__ == "__main__":
    reading_T = threading.Thread(target=working)
    reading_T.start()

    cli_T = threading.Thread(target=cli)
    cli_T.start()
