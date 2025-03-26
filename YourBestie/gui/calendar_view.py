import calendar
from datetime import date
from typing import Callable, cast, override
from dateutil.relativedelta import relativedelta
import flet as ft
from database import event
from . import day_widget

class calendar_view(ft.Column):
    def __init__(self, selected_day: date, on_day_click: Callable[[date], None], team: str):
        super().__init__()
        self._team = team
        self._start_date = selected_day.replace(day=1)
        self._end_date = get_last_date_in_month(selected_day)
        self._selected_day = selected_day
        self._on_day_click = on_day_click
        self.build()

    @override
    def build(self):
        cell_width: int = 80

        self._date_display = ft.TextButton(
            f"{calendar.month_name[self._start_date.month]} {self._start_date.year}",
            on_click=self.open_date_picker_from_month,
            expand=True,
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
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
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

        month_start = self._start_date.weekday()  # Monday=0
        calendar_start = self._start_date + relativedelta(days=-month_start)

        for monthweek in range(6):
            week = ft.Row()
            for wd in range(7):
                offset = monthweek * 7 + wd
                day = calendar_start + relativedelta(days=offset)

                is_in_current_month = (self._start_date <= day <= self._end_date)
                # Filter events based on team.
                day_events = event.calendar_events.get_events_for_day(day, self._team)
                colors_list = [ev.color for ev in day_events]

                widget = day_widget.day_widget(
                    day=day,
                    in_range=is_in_current_month,
                    highlight=(day == self._selected_day),
                    day_click_event=lambda d=day: self.on_day_selected(d),
                    colors=colors_list
                )
                widget.width = cell_width
                widget.height = cell_width
                week.controls.append(widget)
            weeks.append(week)

        self.controls = [self._header, weekday_header] + weeks

    def on_day_selected(self, new_date: date):
        self._selected_day = new_date
        self._on_day_click(new_date)
        self.build()
        self.update_page()

    def open_date_picker_from_month(self, _: ft.ControlEvent):
        date_picker = ft.DatePicker(
            on_change=self.change_month,
            date_picker_mode=ft.DatePickerMode.YEAR,
        )
        self.page.overlay.append(date_picker)
        date_picker.open = True
        self.page.update()

    def change_month(self, event: ft.ControlEvent):
        selection = event.control.value
        if selection is not None:
            self._start_date = selection.replace(day=1)
            self._end_date = get_last_date_in_month(selection)
        self.build()
        self.update_page()

    def prev_month(self, _: ft.ControlEvent):
        self._start_date += relativedelta(months=-1)
        self._end_date = get_last_date_in_month(self._start_date)
        self.build()
        self.update_page()

    def next_month(self, _: ft.ControlEvent):
        self._start_date += relativedelta(months=1)
        self._end_date = get_last_date_in_month(self._start_date)
        self._date_display.text = f"{calendar.month_name[self._start_date.month]} {self._start_date.year}"
        self.build()
        self.update_page()

    def update_page(self):
        cast(ft.Page, self.page).update()

def get_last_date_in_month(day: date):
    import calendar
    return day.replace(day=calendar.monthrange(day.year, day.month)[1])
