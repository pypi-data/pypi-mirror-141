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
from typing import Set

from parallel_utils.thread import create_thread, synchronized

from gpg_multiple_signatures.frontend import Echo, Groups, LiveFields, ProgressMonitors, Terminal
from gpg_multiple_signatures.frontend.verifications import Controller, Messages
from gpg_multiple_signatures.parser import SIGNATURES_EXTENSIONS, verify_parser

ProgressMonitors.gpg.title = 'GPG MULTIPLE VERIFICATIONS'


def verify(folders: Set[Path], threads: int):
    folders = folders or set()
    running_processes = []

    @synchronized()
    def kill_running():
        collections.deque((p.terminate() for p in running_processes), maxlen=0)

    @synchronized(threads)
    def verify(file: Path):
        task = ProgressMonitors.gpg.add_task(description=file.name, total=1, size=file.stat().st_size)
        ProgressMonitors.update_widths()
        search_folders = folders.union([p.resolve() for p in file.parent.iterdir() if p.is_dir()]).union([file.parent])
        signature_files = set((file.with_suffix(f'{file.suffix}.{ext}').name for ext in SIGNATURES_EXTENSIONS))
        signature_file = next((f.resolve() for f in (folder.joinpath(signature_file) for signature_file in signature_files for folder in search_folders)
                               if f.is_file() and not f.is_symlink()), None)
        if not signature_file:
            return Controller.add(task=task, file=file.name, message=Messages.msg_missing)
        if cancel_pending.is_set():
            return Controller.add(task=task, file=file.name, message=Messages.msg_cancelled)
        verification = subprocess.Popen(['gpg', '--verify', signature_file, file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
        running_processes.append(verification)
        verification.communicate()
        if verification.returncode == 0:
            return Controller.add(task=task, file=file.name, message=Messages.msg_good)
        else:
            if verification.returncode in (-15, -9, None):
                return Controller.add(task=task, file=file.name, message=Messages.msg_cancelled)
            else:
                return Controller.add(task=task, file=file.name, message=Messages.msg_bad)

    return verify, kill_running


def signal_handle(signum, frame):
    if cancel_running.is_set():
        return None
    if cancel_pending.is_set():
        cancel_running.set()
        ProgressMonitors.cancelled.add_task(LiveFields.cancelled_second, start=False)
        kill_running()
        return None
    cancel_pending.set()
    ProgressMonitors.cancelled.add_task(LiveFields.cancelled_first.format('Verifications', 'verifications'), start=False)
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
    args = verify_parser.parse_args()
    Terminal.resize(100, 30, strict=False)
    collections.deque((sleep(0.1) if 130 - sum(shutil.get_terminal_size()) >= 10 else None for _ in range(10)), maxlen=0)
    global kill_running
    verify_func, kill_running = verify(folders=args.folders, threads=args.threads)
    LiveFields.overall_description = partial(LiveFields.overall_description.format, total=len(args.files))
    LiveFields.overall_task_id = ProgressMonitors.overall.add_task(LiveFields.overall_description(0), total=len(args.files))
    with LiveFields.table_live:
        for file in args.files:
            threads.append(create_thread(verify_func, file))
        for th in threads:
            th.result()
    Echo.restore_echo_control_characters()


if __name__ == '__main__':
    main()
