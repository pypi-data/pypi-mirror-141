#!/usr/bin/env python3
# encoding:utf-8


from datetime import datetime

from rich.console import RenderableType
from rich.filesize import _to_str
from rich.progress import Task, ProgressColumn, SpinnerColumn, TimeElapsedColumn
from rich.text import Text


class SpinnerTextColumn(SpinnerColumn):
    def __init__(self, *args, finished_text: str = '', **kwargs):
        super().__init__(*args, **kwargs)
        self.finished_text = finished_text

    def render(self, task: "Task") -> RenderableType:
        text = (self.finished_text.format(task=task) if task.finished else self.spinner.render(task.get_time()))
        return text


class TimeStartedColumn(ProgressColumn):
    def __init__(self, *args, style='', **kwargs):
        self.style = style
        super().__init__(*args, **kwargs)

    def render(self, task: "Task") -> Text:
        if task.start_time is None:
            return Text("--:--:--", style=self.style)
        res = datetime.fromtimestamp(task.start_time).strftime('%H:%M:%S')
        return Text(res, style=self.style)


class TimeElapsedStyledColumn(TimeElapsedColumn):
    def __init__(self, *args, style='', **kwargs):
        self.style = style
        super().__init__(*args, **kwargs)

    def render(self, task: "Task") -> Text:
        task = super().render(task)
        return Text(task.plain, style=self.style)


class BinaryFileSizeColumn(ProgressColumn):
    def __init__(self, *args, style='', **kwargs):
        self.style = style
        super().__init__(*args, **kwargs)

    def render(self, task: "Task") -> Text:
        """Show data completed."""
        data_size = _to_str(
            task.fields['size'],
            ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"),
            1024,
        )
        return Text(data_size, style=self.style)
