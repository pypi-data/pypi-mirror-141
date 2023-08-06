#!/usr/bin/env python3
# encoding:utf-8


from parallel_utils.thread import synchronized
from private_attrs import PrivateAttrs
from rich.progress import TaskID
from rich.text import Text

from gpg_multiple_signatures.frontend import Groups, LiveFields, ProgressMonitors


class Messages:
    msg_signed = Text('SIGNED', style='color(4) bold').markup
    msg_skipped = Text('SKIPPED', style='color(3) bold').markup
    msg_error = Text('ERROR', style='color(9) bold').markup
    msg_invalid = Text("ERROR: Destination already exists but it's not a file or it's a symlink!", style='color(9) bold').markup
    msg_cancelled = Text('CANCELLED', style='color(9) bold').markup


def Controller():
    p = PrivateAttrs()

    class Controller():

        def __init__(self):
            p.register_instance(self)

            summary = ProgressMonitors.summary
            signed_task_id = summary.add_task(description=Messages.msg_signed, number=0, start=False, visible=False)
            skipped_task_id = summary.add_task(description=Messages.msg_skipped, number=0, start=False, visible=False)
            error_task_id = summary.add_task(description=Text('ERRORS', style='color(9) bold').markup, number=0, start=False, visible=False)
            cancelled_task_id = summary.add_task(description=Messages.msg_cancelled, number=0, start=False, visible=False)
            summary_tasks = summary.tasks

            self.signed_task = next(t for t in summary_tasks if t.id == signed_task_id)
            self.skipped_task = next(t for t in summary_tasks if t.id == skipped_task_id)
            self.error_task = next(t for t in summary_tasks if t.id == error_task_id)
            self.cancelled_task = next(t for t in summary_tasks if t.id == cancelled_task_id)

            p.action_dict = {
                Messages.msg_signed: lambda: summary.update(signed_task_id, number=self.signed + 1, visible=True),
                Messages.msg_skipped: lambda: summary.update(skipped_task_id, number=self.skipped + 1, visible=True),
                Messages.msg_error: lambda: summary.update(error_task_id, number=self.error + 1, visible=True),
                Messages.msg_invalid: lambda: summary.update(error_task_id, number=self.error + 1, visible=True),
                Messages.msg_cancelled: lambda: summary.update(cancelled_task_id, number=self.cancelled + 1, visible=True),
                # Messages.msg_invalid: lambda: p.get_private_attr(self, 'action_dict')[Messages.msg_error]()
            }

        def __del__(self):
            p.delete(self)

        @synchronized()
        def add(self, task: TaskID, file: str, message: str):
            p.action_dict[message]()
            if LiveFields.table_live.get_renderable() is Groups.initial:
                LiveFields.table_live.update(Groups.final)
            elif LiveFields.table_live.get_renderable() is Groups.initial_cancelled:
                LiveFields.table_live.update(Groups.final_cancelled)
            ProgressMonitors.gpg.update(task, description=file, status=message, advance=1)
            if message is not Messages.msg_cancelled:
                ProgressMonitors.overall.update(LiveFields.overall_task_id, description=LiveFields.overall_description(self.total_processed), advance=1)

        @property
        def signed(self):
            return self.signed_task.fields['number']

        @property
        def skipped(self):
            return self.skipped_task.fields['number']

        @property
        def error(self):
            return self.error_task.fields['number']

        @property
        def cancelled(self):
            return self.cancelled_task.fields['number']

        @property
        def total_processed(self):
            return self.signed + self.skipped + self.error

    Controller.__qualname__ = 'Controller'

    return Controller


Controller = Controller()()
