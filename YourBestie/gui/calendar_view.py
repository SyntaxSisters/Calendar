import calendar
from datetime import date
from typing import Callable, cast, override
from dateutil.relativedelta import relativedelta
import flet as ft
from database import event
from . import day_widget

class calendar_view(ft.Column):
    _selected_day: date
    _date_error: ft.Text = ft.Text("", color=ft.Colors.ON_ERROR, size=14)
    _start_date: date
    _end_date: date
    _date_display:ft.TextButton # pyright: ignore[reportUninitializedInstanceVariable]
    _on_day_click: Callable[[date], None]
    _header:ft.Row # pyright: ignore[reportUninitializedInstanceVariable]
    def __init__(
        self, selected_day:date, on_day_click: Callable[[date], None]
    ):
        _: None = super().__init__()  # pyright: ignore[reportUnknownMemberType]
        self._start_date = selected_day + relativedelta(day=1)
        self._end_date = get_last_date_in_month(selected_day)
        self._selected_day = selected_day
        self._on_day_click = on_day_click

    @override    
    def build(self):
        cell_width: int = 80
        self._date_display = ft.TextButton(
                    f"{calendar.month_name[self._start_date.month]} {self._end_date.year}",
                    on_click=self.open_date_picker_from_month,
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

        weeks: list[ft.Control] = []
        
        month_start = self._start_date.weekday()
        calendar_start = self._start_date + relativedelta(days=-month_start)
        
        for monthweek in range(6):
            week = ft.Row()
            for weekday in range(7):
                offset = monthweek*7 + weekday
                day = calendar_start + relativedelta(days=offset)
                
                is_in_current_month:bool = day >= self._start_date and day <= self._end_date
                widget = day_widget.day_widget(
                    day, 
                    highlight=day == self._selected_day, 
                    in_range=is_in_current_month,
                    event_count=len(event.calendar_events.get_events_for_day(day)),
                    day_click_event=self._on_day_click)
                widget.width = cell_width
                widget.height = cell_width
                week.controls.append(widget)
            weeks.append(week)

        self.controls: list[ft.Control] = [self._header, weekday_header] + weeks

    def prev_month(self, _: ft.ControlEvent):
        """Change the current stored month to the previous month

        Args:
            event (ft.ControlEvent): A button click event
        """
        self._start_date += relativedelta(months=-1)
        self._end_date = get_last_date_in_month(self._start_date)
        self.build()
        cast(Callable[...,None],cast(ft.Page,self.page).update)()

    def next_month(self, _: ft.ControlEvent):
        """Change the current stored month to the next month

        Args:
            event (ft.ControlEvent): A button click event
        """
        self._start_date += relativedelta(months=1)
        self._end_date = get_last_date_in_month(self._start_date)
        self._date_display.text=f"{calendar.month_name[self._start_date.month]} {self._start_date.year}"
        self.build()
        cast(Callable[...,None],cast(ft.Page,self.page).update)()

    def change_month(self, event:ft.ControlEvent):
        selection =  cast(ft.DatePicker,event.control).value
        if selection is not None:
            self._start_date = selection + relativedelta(day=1)
            self._end_date = get_last_date_in_month(selection)
        self.build()
        cast(Callable[...,None],cast(ft.Page,self.page).update)()

    def open_date_picker_from_month(self, _: ft.ControlEvent):
        """Display a date picker

        Args:
            event (ft.ControlEvent): A button click event
        """
        cast(ft.Page,self.page).open(
            ft.DatePicker(
                on_change=self.change_month,
                date_picker_mode=ft.DatePickerMode.YEAR
            )
        )

def get_last_date_in_month(day: date):
    return day + relativedelta(
        day=calendar.monthrange(date.today().year, date.today().month)[1]
    )