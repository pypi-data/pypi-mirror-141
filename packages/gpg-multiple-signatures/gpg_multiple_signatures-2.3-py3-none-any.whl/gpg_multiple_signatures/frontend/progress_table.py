#!/usr/bin/env python3
# encoding:utf-8


from typing import Union, Iterable, Optional, Sequence

from rich import box
from rich.console import JustifyMethod
from rich.padding import PaddingDimensions, Padding
from rich.progress import Progress, Task, ProgressColumn
from rich.style import StyleType
from rich.table import Table, Column
from rich.text import TextType


class ProgressTable(Progress):
    def __init__(self,
                 *columns: Union[str, ProgressColumn],
                 title: Optional[TextType] = None,
                 caption: Optional[TextType] = None,
                 width: Optional[int] = None,
                 min_width: Optional[int] = None,
                 box: Optional[box.Box] = box.HEAVY_HEAD,
                 safe_box: Optional[bool] = None,
                 padding: PaddingDimensions = (0, 1),
                 collapse_padding: bool = False,
                 pad_edge: bool = True,
                 show_header: bool = True,
                 show_footer: bool = False,
                 show_edge: bool = True,
                 show_lines: bool = False,
                 leading: int = 0,
                 style: StyleType = "none",
                 row_styles: Optional[Iterable[StyleType]] = None,
                 header_style: Optional[StyleType] = "table.header",
                 footer_style: Optional[StyleType] = "table.footer",
                 border_style: Optional[StyleType] = None,
                 title_style: Optional[StyleType] = None,
                 caption_style: Optional[StyleType] = None,
                 title_justify: "JustifyMethod" = "center",
                 caption_justify: "JustifyMethod" = "center",
                 highlight: bool = False,
                 **kwargs):
        self.title = title
        self.caption = caption
        self.width = width
        self.min_width = min_width
        self.box = box
        self.safe_box = safe_box
        self._padding = Padding.unpack(padding)
        self.pad_edge = pad_edge
        self.show_header = show_header
        self.show_footer = show_footer
        self.show_edge = show_edge
        self.show_lines = show_lines
        self.leading = leading
        self.collapse_padding = collapse_padding
        self.style = style
        self.header_style = header_style or ""
        self.footer_style = footer_style or ""
        self.border_style = border_style
        self.title_style = title_style
        self.caption_style = caption_style
        self.title_justify: "JustifyMethod" = title_justify
        self.caption_justify: "JustifyMethod" = caption_justify
        self.highlight = highlight
        self.row_styles: Sequence[StyleType] = list(row_styles or [])
        super().__init__(*columns, **kwargs)

    def make_tasks_table(self, tasks: Iterable[Task]) -> Table:
        table_columns = ((Column(no_wrap=True) if isinstance(_column, str) else _column.get_table_column().copy()) for _column in self.columns)
        table = Table(*table_columns, title=self.title, caption=self.caption, width=self.width, min_width=self.min_width, box=self.box, safe_box=self.safe_box, padding=self._padding,
                      expand=self.expand, pad_edge=self.pad_edge, show_header=self.show_header, show_footer=self.show_footer, show_edge=self.show_edge, show_lines=self.show_lines,
                      leading=self.leading, collapse_padding=self.collapse_padding, style=self.style, header_style=self.header_style, footer_style=self.footer_style, border_style=self.border_style,
                      title_style=self.title_style, caption_style=self.caption_style, title_justify=self.title_justify, caption_justify=self.caption_justify, highlight=self.highlight,
                      row_styles=self.row_styles)

        for task in tasks:
            if task.visible:
                table.add_row(*((column.format(task=task) if isinstance(column, str) else column(task)) for column in self.columns))
        return table
