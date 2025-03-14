import calendar
from datetime import date
from typing import Callable, override
from dateutil.relativedelta import relativedelta
import flet as ft

import utils

class calendar_view(ft.Column):
    _selected_day: ft.Text = ft.Text("", size=18, color=ft.Colors.ON_SURFACE)
    _date_error: ft.Text = ft.Text("", color=ft.Colors.ON_ERROR, size=14)
    _start_date: date
    _end_date: date
    _date_display:ft.TextButton
    _on_day_click: Callable[[int], None]
    _header:ft.Row
    def __init__(
        self, start_date: date, end_date: date, on_day_click: Callable[[int], None]
    ):
        _: None = super().__init__()  # pyright: ignore[reportUnknownMemberType]
        self._start_date = start_date
        self._end_date = start_date
        self._on_day_click = on_day_click
        self._date_display = ft.TextButton(
                    f"{calendar.month_name[self._start_date.month]} {self._end_date.year}"
                    # on_click=open_date_picker_from_month,
                )
        self._header = ft.Row(
            [
                ft.IconButton(
                    ft.Icons.ARROW_LEFT,
                    on_click=self.prev_month,
                    tooltip="Previous Month",
                    width=40,
                ),
                self._date_display,
                ft.IconButton(
                    ft.Icons.ARROW_RIGHT,
                    on_click=self.next_month,
                    tooltip="Next Month",
                    width=40,
                ),
            ]
        )

    @override    
    def build(self):
        cell_width: int = 80
        cal = calendar.monthcalendar(self._start_date.year, self._start_date.month)
        self._date_display = ft.TextButton(
                    f"{calendar.month_name[self._start_date.month]} {self._end_date.year}"
                    # on_click=open_date_picker_from_month,
                )
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self._header = ft.Row(
            [
                ft.IconButton(
                    ft.Icons.ARROW_LEFT,
                    on_click=self.prev_month,
                    tooltip="Previous Month",
                    width=40,
                ),
                self._date_display,
                ft.IconButton(
                    ft.Icons.ARROW_RIGHT,
                    on_click=self.next_month,
                    tooltip="Next Month",
                    width=40,
                ),
            ]
        )
        weekday_header = ft.Container(
            ft.Row(
                [
                    ft.Text(
                        day,
                        size=24,
                        width=cell_width,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.ON_PRIMARY,
                    )
                    for day in weekdays
                ],
            ),
            bgcolor=ft.Colors.PRIMARY,
        )

        days_grid: list[ft.Control] = []
        for week in cal:
            days_grid.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                str(day) if day != 0 else "",
                                size=24,
                                color=ft.Colors.ON_PRIMARY_CONTAINER,
                            ),
                            width=cell_width,
                            height=cell_width,
                            bgcolor=ft.Colors.PRIMARY_CONTAINER
                            if day != 0
                            else "transparent",
                            border_radius=5,
                            border=ft.border.all(1, "white"),
                            alignment=ft.alignment.center,
                            on_click=lambda e, d=day: self._on_day_click(d) if d != 0 else None,
                        )
                        for day in week
                    ]
                )
            )
        self.controls: list[ft.Control] = [self._header, weekday_header] + days_grid

    def prev_month(self, event: ft.ControlEvent):
        """Change the current stored month to the previous month

        Args:
            event (ft.ControlEvent): A button click event
        """
        self._start_date += relativedelta(months=-1)
        self._end_date = utils.get_last_date_in_month(self._start_date)
        self._date_display = ft.TextButton(
            f"{calendar.month_name[self._start_date.month]} {self._start_date.year}"
            # on_click=open_date_picker_from_month,
        )
        self.build()
        self.page.update() # pyright: ignore[reportUnknownMemberType, reportOptionalMemberAccess]

    def next_month(self, event: ft.ControlEvent):
        """Change the current stored month to the next month

        Args:
            event (ft.ControlEvent): A button click event
        """
        self._start_date += relativedelta(months=1)
        self._end_date = utils.get_last_date_in_month(self._start_date)
        self._date_display = ft.TextButton(
            f"{calendar.month_name[self._start_date.month]} {self._start_date.year}"
            # on_click=open_date_picker_from_month,
        )
        self.build()
        self.page.update() # pyright: ignore[reportUnknownMemberType, reportOptionalMemberAccess]
