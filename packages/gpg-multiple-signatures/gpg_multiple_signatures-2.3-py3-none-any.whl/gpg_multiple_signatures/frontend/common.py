#!/usr/bin/env python3
# encoding:utf-8


import time

from rich import box
from rich.align import Align
from rich.console import Group, Console
from rich.live import Live
from rich.measure import Measurement
from rich.padding import Padding
from rich.progress import Progress, TextColumn, BarColumn
from rich.table import Column
from rich.text import Text

from gpg_multiple_signatures.frontend.columns import BinaryFileSizeColumn, TimeElapsedStyledColumn, TimeStartedColumn, SpinnerTextColumn
from gpg_multiple_signatures.frontend.progress_table import ProgressTable

console = Console(highlight=False)


class ProgressMonitors:
    gpg = ProgressTable(
        TimeStartedColumn(table_column=Column(header='TIME STARTED', justify='center'), style='color(12)'),
        TimeElapsedStyledColumn(table_column=Column(header='TIME ELAPSED', justify='center'), style='color(14)'),
        TextColumn('{task.description}', table_column=Column(header=Align.center('FILE'))),
        BinaryFileSizeColumn(table_column=Column(header=Align.center('SIZE'), style='color(177)')),
        SpinnerTextColumn(spinner_name='point', table_column=Column(header='STATUS', justify='center'), finished_text='{task.fields[status]}', style='white'),
        title='',
        title_style='bold',
        box=box.HORIZONTALS,
        padding=(0, 1),
        get_time=time.time,
    )

    bar = BarColumn()
    overall = Progress(
        TimeElapsedStyledColumn(style='color(48)'), '•', bar, TextColumn('[color(48)]{task.percentage:.2f}%'), '•', TextColumn('{task.description}')
    )

    summary = ProgressTable(TextColumn('{task.description}', table_column=Column(justify='right')),
                            TextColumn('[bold]{task.fields[number]}', table_column=Column(justify='center')),
                            title=Text('SUMMARY OF EXECUTION').markup,
                            title_style='bold',
                            min_width=20,
                            box=box.HORIZONTALS,
                            show_lines=True,
                            show_header=False)

    cancelled_column = Column()
    cancelled = Progress(TextColumn('{task.description}', justify='full', table_column=cancelled_column))

    @classmethod
    def update_widths(cls):
        gpg_measures = Measurement.get(console=console, options=console.options, renderable=cls.gpg)
        cls.bar.bar_width = min(40, gpg_measures.maximum - 43)
        cls.cancelled_column.max_width = gpg_measures.maximum - 7
        LiveFields.table_live.update(LiveFields.table_live.get_renderable())


class Groups:
    complete = (
        Padding(ProgressMonitors.gpg, (1, 3, 1, 3)),
        Padding(ProgressMonitors.overall, (0, 3, 1, 5)),
        Padding(ProgressMonitors.summary, (0, 3, 1, 5)),
        Padding(ProgressMonitors.cancelled, (0, 3, 1, 5)),
    )

    initial = Group(*complete[0:2])

    initial_cancelled = Group(*(initial, complete[3]))

    final = Group(*complete[0:3])

    final_cancelled = Group(*complete)


class LiveFields:
    overall_description = Text('{}/{total} files processed', style='color(192)').markup
    cancelled_first = Text('Process stop requested. All pending tasks have been cancelled.\n{} in progress will continue to run until complete.\n\n'
                           'To stop the execution of the {} in progress,\nmake another request to stop the program completely.',
                           style='color(202) bold').markup
    cancelled_second = Text('\nCanceling all running tasks and exiting...', style='color(202) bold').markup
    overall_task_id = None
    table_live = Live(Groups.initial, console=console, refresh_per_second=20)
