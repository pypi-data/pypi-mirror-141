#!/usr/bin/env python3
# encoding:utf-8


import copy
import os
import shutil
import subprocess
import sys
import termios
from typing import Tuple


class Echo:
    disable_echo_control_characters = lambda x=None: None
    restore_echo_control_characters = lambda x=None: None

    @classmethod
    def configure_echo_control_characters(cls):
        '''
        Create methods for enabling and disabling the printing of some inputs as Control+C (^C)
        The optional argument x=None is required in case the method is called with self or cls as first argument
        '''
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = copy.deepcopy(old)
            new[3] = new[3] & ~termios.ECHOCTL
            cls.disable_echo_control_characters = lambda x=None: termios.tcsetattr(fd, termios.TCSADRAIN, new)
            cls.restore_echo_control_characters = lambda x=None: termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except termios.error:
            print('Error: Could not configure echo control characters', file=sys.stderr)


class Terminal:
    @classmethod
    def get_size(cls) -> Tuple[int, int]:
        width, height = shutil.get_terminal_size()
        if os.environ.get('TMUX', default=None) is not None:
            subprocess.run(['tmux', 'set', '-g', 'status', 'off'], capture_output=True)
            height = subprocess.run(['tmux', 'display-message', '-p', '#{window_height}'], capture_output=True, text=True).stdout
            width = subprocess.run(['tmux', 'display-message', '-p', '#{window_width}'], capture_output=True, text=True).stdout
            subprocess.run(['tmux', 'set', '-g', 'status', 'on'], capture_output=True)
            width, height = int(width), int(height)
        return width, height

    @classmethod
    def resize(cls, width: int = 0, height: int = 0, strict: bool = False):
        """
        Resizes the console (https://superuser.com/a/689846)
        """
        if os.environ.get('TERM', default=None) == 'linux':  # For pure tty terminals instead of terminal emulators
            return
        width_orig, height_orig = cls.get_size()
        width = width_orig if not width else width
        height = height_orig if not height else height
        if not strict:
            width, height = max(width, width_orig), max(height, height_orig)
        resize_string = f'\033[8;{height};{width}t'  # Byte \033 represents \e (Can also be written as \x1b)
        if os.environ.get('TMUX', default=None) is not None:
            resize_string = f'\033Ptmux;\033\033[8;{height};{width}t\033\\'
        print(resize_string, end='', flush=True)


Echo.configure_echo_control_characters()
