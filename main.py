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

message = Queue()


def working():
    p1 = Panel('192.168.0.101', 'P1')
    p2 = Panel('192.168.0.102', 'P2')
    p3 = Panel('192.168.0.103', 'P3')
    p4 = Panel('192.168.0.104', 'P4')
    p5 = Panel('192.168.0.105', 'P5')
    p6 = Panel('192.168.0.106', 'P6')
    p7 = Panel('192.168.0.107', 'P7')
    p8 = Panel('192.168.0.108', 'P8')
    panels = [p1, p2, p3, p4, p5, p6, p7, p8]

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
                panel.save_data()
            print(' Done ', end='', flush=True)

        elif cmd == 'CLEAR':
            for panel in panels:
                panel.clear_data()
            print(' Done ', end='', flush=True)

        elif cmd == 'NEW':
            for panel in panels:
                panel.save_data()

            for panel in panels:
                panel.clear_data()

            print(' Done ', end='', flush=True)


def cli():
    import curses

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.addstr(0, 40, "Welcome to the AC/DC meter data panel", curses.A_REVERSE)
    stdscr.addstr(1, 0, "<s> (save) to save data", curses.color_pair(1))
    stdscr.addstr(2, 0, "<c> (clear) to clear data", curses.color_pair(1))
    stdscr.addstr(3, 0, "<n> (new) to save and start new session\n", curses.color_pair(1))

    line = 4

    while True:
        stdscr.refresh()
        c = stdscr.getch()
        if c == ord('s'):
            message.put('SAVE')
            stdscr.addstr(line, 0, 'Saving current session ...')
            line += 1

        elif c == ord('c'):
            stdscr.addstr(line, 0, 'Clear current data ...')
            message.put('CLEAR')
            line += 1

        elif c == ord('n'):
            stdscr.addstr(line, 0, 'Saving current session and start new one ...')
            message.put('NEW')
            line += 1


if __name__ == "__main__":
    import threading

    reading_T = threading.Thread(target=working)
    reading_T.start()

    cli_T = threading.Thread(target=cli)
    cli_T.start()
