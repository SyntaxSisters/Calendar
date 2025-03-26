# calendar_view.py
import calendar
from datetime import date
from typing import Callable, cast, override
from dateutil.relativedelta import relativedelta
import flet as ft
from database import event
from . import day_widget

class calendar_view(ft.Column):
    """
    A calendar that can display in either 'month view' or 'week view'.
    The user can toggle between views using a button in the header.
    """

    def __init__(self, selected_day: date, on_day_click: Callable[[date], None], team: str):
        super().__init__()
        # store parameters
        self._team = team
        self._selected_day = selected_day
        self._on_day_click = on_day_click

        # start in Month View
        self._is_week_view = False

        # month view, track the start/end of the month
        self._start_date = selected_day.replace(day=1)
        self._end_date = get_last_date_in_month(selected_day)

        self.build()

    @override
    def build(self):
        """Builds the entire calendar layout depending on whether it's week view or month view."""
        self.controls.clear()  # clear old controls before rebuilding

        cell_width: int = 80

        # toggle button that flips between 'week View' and 'month View'
        self._toggle_button = ft.TextButton(
            "Week View" if not self._is_week_view else "Month View",
            on_click=self.toggle_view_mode,
            expand=False,
        )

        if self._is_week_view:
            # WEEK VIEW
            # the Monday of the selected week's row (Monday=0)
            start_of_week = self._selected_day - relativedelta(days=self._selected_day.weekday())
            end_of_week = start_of_week + relativedelta(days=6)
            date_display_text = f"Week of {start_of_week.strftime('%b %d')} - {end_of_week.strftime('%b %d, %Y')}"
        else:
            # MONTH VIEW
            date_display_text = f"{calendar.month_name[self._start_date.month]} {self._start_date.year}"

        self._date_display = ft.TextButton(
            date_display_text,
            on_click=self.open_date_picker_from_month if not self._is_week_view else None,
            expand=True,
        )

        # arrow buttons
        prev_button = ft.IconButton(
            ft.Icons.ARROW_LEFT,
            on_click=self.prev_period,
            tooltip="Previous",
            width=40,
        )
        next_button = ft.IconButton(
            ft.Icons.ARROW_RIGHT,
            on_click=self.next_period,
            tooltip="Next",
            width=40,
        )

        self._header = ft.Row(
            [
                prev_button,
                self._date_display,
                self._toggle_button,
                next_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        # build weekday
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

        if self._is_week_view:
            # WEEK VIEW -> only 1 row (7 days)
            rows = [self.build_week_row()]
        else:
            # MONTH VIEW -> up to 6 rows
            rows = self.build_month_rows()

        self.controls.append(self._header)
        self.controls.append(weekday_header)
        self.controls.extend(rows)

    def build_month_rows(self) -> list[ft.Row]:
        """
        Builds up to 6 weeks' worth of rows for the selected month.
        """
        rows: list[ft.Row] = []
        cell_width = 80

        month_start_wkday = self._start_date.weekday()  # Monday=0
        calendar_start = self._start_date - relativedelta(days=month_start_wkday)

        for week_idx in range(6):
            week_row = ft.Row()
            for wd in range(7):
                offset = week_idx * 7 + wd
                day = calendar_start + relativedelta(days=offset)

                is_in_current_month = (self._start_date <= day <= self._end_date)
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
                week_row.controls.append(widget)
            rows.append(week_row)

        return rows

    def build_week_row(self) -> ft.Row:
        """
        Builds a single row containing 7 days: the week containing self._selected_day.
        """
        week_row = ft.Row()
        cell_width = 80

        start_of_week = self._selected_day - relativedelta(days=self._selected_day.weekday())

        for i in range(7):
            day = start_of_week + relativedelta(days=i)
            day_events = event.calendar_events.get_events_for_day(day, self._team)
            colors_list = [ev.color for ev in day_events]

            widget = day_widget.day_widget(
                day=day,
                in_range=True,  # We consider the entire week in range
                highlight=(day == self._selected_day),
                day_click_event=lambda d=day: self.on_day_selected(d),
                colors=colors_list
            )
            widget.width = cell_width
            widget.height = cell_width
            week_row.controls.append(widget)

        return week_row

    def on_day_selected(self, new_date: date):
        """
        Called when a user clicks a day in either month or week view.
        """
        self._selected_day = new_date
        if not self._is_week_view:
            
            pass
        else:
            pass

        self.build()
        self.update_page()
        self._on_day_click(new_date)

    def open_date_picker_from_month(self, _: ft.ControlEvent):
        """
        Opens a date picker to jump to another month/year.
        Only used in month view.
        """
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
            self._selected_day = selection
        self.build()
        self.update_page()

    def prev_period(self, _: ft.ControlEvent):
        """
        Called when user clicks the left arrow.
        If we're in week view, go one week back.
        If we're in month view, go one month back.
        """
        if self._is_week_view:
            self._selected_day -= relativedelta(weeks=1)
        else:
            self._start_date -= relativedelta(months=1)
            self._selected_day = self._start_date
            self._end_date = get_last_date_in_month(self._start_date)

        self.build()
        self.update_page()

    def next_period(self, _: ft.ControlEvent):
        """
        Called when user clicks the right arrow.
        If we're in week view, go one week forward.
        If we're in month view, go one month forward.
        """
        if self._is_week_view:
            self._selected_day += relativedelta(weeks=1)
        else:
            self._start_date += relativedelta(months=1)
            self._selected_day = self._start_date
            self._end_date = get_last_date_in_month(self._start_date)

        self.build()
        self.update_page()

    def toggle_view_mode(self, _: ft.ControlEvent):
        """
        Toggle between month view and week view.
        """
        self._is_week_view = not self._is_week_view

        if not self._is_week_view:
            self._start_date = self._selected_day.replace(day=1)
            self._end_date = get_last_date_in_month(self._start_date)

        self.build()
        self.update_page()

    def update_page(self):
        cast(ft.Page, self.page).update()


def get_last_date_in_month(day: date):
    import calendar
    return day.replace(day=calendar.monthrange(day.year, day.month)[1])
