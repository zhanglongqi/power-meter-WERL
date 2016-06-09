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
from queue import Empty
import os, threading

from message import message


def worker():
    p1 = Panel('192.168.0.101', 'P1')
    p2 = Panel('192.168.0.102', 'P2')
    p3 = Panel('192.168.0.103', 'P3')
    p4 = Panel('192.168.0.104', 'P4')
    p5 = Panel('192.168.0.105', 'P5')
    p6 = Panel('192.168.0.106', 'P6')
    p7 = Panel('192.168.0.107', 'P7')
    p8 = Panel('192.168.0.108', 'P8')
    all_panels = ['_', p1, p2, p3, p4, p5, p6, p7, p8]
    panels = []

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
            sleep(1)  # todo this will slow down the response

        elif cmd.isdigit():
            if all_panels[int(cmd)] in panels:
                panels.remove(all_panels[int(cmd)])
                print('\rRemove panel ' + cmd + ' from list\n')
            else:
                panels.append(all_panels[int(cmd)])
                print('\rPut panel ' + cmd + ' to list\n')

        elif cmd == 'SAVE':
            for panel in panels:
                panel.save_data_spreadsheet()
            for panel in panels:
                panel.clear_data()
            print('\r Done \n')

        elif cmd == 'CLEAR':
            for panel in panels:
                panel.clear_data()
            print('\r Done \n')

        elif cmd == 'NEW':
            for panel in panels:
                panel.save_data_spreadsheet()

            for panel in panels:
                panel.clear_data()

            print('\r Done \n')


def print_help_message():
    print('''\n
        ****************************************************************************\n
        *****************   Welcome to the AC/DC meter data panel  *****************\n
        ****                    <s> (save) to save data                         ****\n
        ****                    <c> (clear) to clear previous data              ****\n
        ****                    <n> (new) to save and start new session         ****\n
        ****                    <q> (quit) to quit the app                      ****\n
        ****                                                                    ****\n
        ****                    < 1, 2, 3, 4, 5, 6, 7, 8 >                      ****\n
        ****              press number to add/remove corresponding panel        ****\n
        ****************************************************************************\n
        ''', flush=True)


def cli():
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
        import curses
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        stdscr.addstr(0, 20, "****************************************************************************",
                      curses.color_pair(1))
        stdscr.addstr(1, 20, "*****************   Welcome to the AC/DC meter data panel  *****************\n",
                      curses.color_pair(1))
        stdscr.addstr(2, 20, "****                    <s> (save) to save data                         ****\n",
                      curses.color_pair(1))
        stdscr.addstr(3, 20, "****                    <c> (clear) to clear previous data              ****\n",
                      curses.color_pair(1))
        stdscr.addstr(4, 20, "****                    <n> (new) to save and start new session         ****\n",
                      curses.color_pair(1))
        stdscr.addstr(5, 20, "****                    <q> (quit) to quit the app                      ****\n",
                      curses.color_pair(1))
        stdscr.addstr(6, 20, "****                                                                    ****\n",
                      curses.color_pair(1))
        stdscr.addstr(7, 20, "****                    < 1, 2, 3, 4, 5, 6, 7, 8 >                      ****\n",
                      curses.color_pair(1))
        stdscr.addstr(8, 20, "****              press number to add/remove corresponding panel        ****\n",
                      curses.color_pair(1))
        stdscr.addstr(9, 20, "****************************************************************************\n",
                      curses.color_pair(1))

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

        def getchar():
            cmd = stdscr.getch()
            return chr(cmd)

    while True:
        cmd = getchar()
        if cmd == 'q':
            # message.put('QUIT')
            raise KeyboardInterrupt

        if cmd == 's':
            message.put('SAVE')
            print('\rSaving current session ...', end='')

        elif cmd == 'c':
            print('\rClear current data ...', end='')
            message.put('CLEAR')

        elif cmd == 'n':
            print('\rSaving current session and start new one ...', end='')
            message.put('NEW')

        elif cmd.isdigit():  # put corresponding panel to list
            message.put(cmd)


if __name__ == "__main__":
    reading_T = threading.Thread(target=worker, daemon=True)
    reading_T.start()

    cli_T = threading.Thread(target=cli)
    cli_T.start()
