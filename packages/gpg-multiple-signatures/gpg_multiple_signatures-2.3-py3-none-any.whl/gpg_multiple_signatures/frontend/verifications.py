#!/usr/bin/env python3
# encoding:utf-8


from parallel_utils.thread import synchronized
from private_attrs import PrivateAttrs
from rich.progress import TaskID
from rich.text import Text

from gpg_multiple_signatures.frontend import Groups, LiveFields, ProgressMonitors


class Messages:
    msg_good = Text('GOOD', style='color(2) bold').markup
    msg_missing = Text('MISSING', style='color(3) bold').markup
    msg_bad = Text('BAD', style='color(9) bold').markup
    msg_cancelled = Text('CANCELLED', style='color(9) bold').markup


def Controller():
    p = PrivateAttrs()

    class Controller:

        def __init__(self):
            p.register_instance(self)

            summary = ProgressMonitors.summary
            good_task_id = summary.add_task(description=Messages.msg_good, number=0, start=False, visible=False)
            missing_task_id = summary.add_task(description=Messages.msg_missing, number=0, start=False, visible=False)
            bad_task_id = summary.add_task(description=Messages.msg_bad, number=0, start=False, visible=False)
            cancelled_task_id = summary.add_task(description=Messages.msg_cancelled, number=0, start=False, visible=False)
            summary_tasks = summary.tasks

            self.good_task = next((t for t in summary_tasks if t.id == good_task_id))
            self.missing_task = next((t for t in summary_tasks if t.id == missing_task_id))
            self.bad_task = next((t for t in summary_tasks if t.id == bad_task_id))
            self.cancelled_task = next(t for t in summary_tasks if t.id == cancelled_task_id)

            p.action_dict = {
                Messages.msg_good: lambda: summary.update(good_task_id, number=self.good + 1, visible=True),
                Messages.msg_missing: lambda: summary.update(missing_task_id, number=self.missing + 1, visible=True),
                Messages.msg_bad: lambda: summary.update(bad_task_id, number=self.bad + 1, visible=True),
                Messages.msg_cancelled: lambda: summary.update(cancelled_task_id, number=self.cancelled + 1, visible=True),
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
        def good(self):
            return self.good_task.fields['number']

        @property
        def missing(self):
            return self.missing_task.fields['number']

        @property
        def bad(self):
            return self.bad_task.fields['number']

        @property
        def cancelled(self):
            return self.cancelled_task.fields['number']

        @property
        def total_processed(self):
            return self.good + self.missing + self.bad

    Controller.__qualname__ = 'Controller'

    return Controller


Controller = Controller()()
