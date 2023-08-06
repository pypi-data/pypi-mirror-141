#!/usr/bin/env python3
# encoding:utf-8


import collections
import shutil
import signal
import subprocess
from functools import partial
from pathlib import Path
from threading import Event
from time import sleep
from typing import List

from parallel_utils.thread import create_thread, synchronized

from gpg_multiple_signatures.frontend import Echo, Groups, LiveFields, ProgressMonitors, Terminal
from gpg_multiple_signatures.frontend.signatures import Controller, Messages
from gpg_multiple_signatures.parser import sign_parser

ProgressMonitors.gpg.title = 'GPG MULTIPLE SIGNATURES'


def sign(binary: bool, destination: Path, extension: str, overwrite: bool, threads: int, users: List[str]):
    users = users or tuple()
    running_processes = []

    @synchronized()
    def kill_running():
        collections.deque((p.terminate() for p in running_processes), maxlen=0)

    @synchronized(threads)
    def sign(file: Path):
        task = ProgressMonitors.gpg.add_task(description=file.name, total=1, size=file.stat().st_size)
        ProgressMonitors.update_widths()
        dest = destination or file.parent
        dest = dest.joinpath(f'{file.name}.{extension}')
        if dest.exists():
            if not dest.is_file() or dest.is_symlink():
                return Controller.add(task=task, file=str(dest), message=Messages.msg_invalid)
            if not overwrite:
                return Controller.add(task=task, file=file.name, message=Messages.msg_skipped)
        if cancel_pending.is_set():
            return Controller.add(task=task, file=file.name, message=Messages.msg_cancelled)
        command = ['gpg', '-o', str(dest), '--detach-sign']
        if not binary:
            command.append('-a')
        if overwrite:
            command.extend(('--batch', '--yes'))
        for user in users:
            command.extend(('-u', user))
        command.append(file)
        dest.parent.mkdir(exist_ok=True)
        sign = subprocess.Popen(command, start_new_session=True, stderr=subprocess.PIPE)
        running_processes.append(sign)
        sign.communicate()
        if sign.returncode == 0:
            return Controller.add(task=task, file=file.name, message=Messages.msg_signed)
        else:
            try:
                dest.unlink()
            except FileNotFoundError:
                pass
            if sign.returncode in (-15, -9, None):
                return Controller.add(task=task, file=file.name, message=Messages.msg_cancelled)
            else:
                return Controller.add(task=task, file=file.name, message=Messages.msg_error)

    return sign, kill_running


def signal_handle(signum, frame):
    if cancel_running.is_set():
        return None
    if cancel_pending.is_set():
        cancel_running.set()
        ProgressMonitors.cancelled.add_task(LiveFields.cancelled_second, start=False)
        kill_running()
        return None
    cancel_pending.set()
    ProgressMonitors.cancelled.add_task(LiveFields.cancelled_first.format('Signatures', 'signatures'), start=False)
    if LiveFields.table_live.get_renderable() is Groups.initial:
        LiveFields.table_live.update(Groups.initial_cancelled)
    else:
        LiveFields.table_live.update(Groups.final_cancelled)


threads = []
cancel_pending = Event()
cancel_running = Event()
kill_running = None

signal.signal(signal.SIGINT, signal_handle)
signal.signal(signal.SIGTERM, signal_handle)


def main():
    Echo.disable_echo_control_characters()
    args = sign_parser.parse_args()
    Terminal.resize(100, 30, strict=False)
    collections.deque((sleep(0.1) if 130 - sum(shutil.get_terminal_size()) >= 10 else None for _ in range(10)), maxlen=0)
    global kill_running
    sign_func, kill_running = sign(binary=args.binary, destination=args.destination, extension=args.extension, overwrite=args.overwrite, threads=args.threads, users=args.users)
    LiveFields.overall_description = partial(LiveFields.overall_description.format, total=len(args.files))
    LiveFields.overall_task_id = ProgressMonitors.overall.add_task(LiveFields.overall_description(0), total=len(args.files))
    with LiveFields.table_live:
        for file in args.files:
            threads.append(create_thread(sign_func, file))
        for th in threads:
            th.result()
    Echo.restore_echo_control_characters()


if __name__ == '__main__':
    main()
