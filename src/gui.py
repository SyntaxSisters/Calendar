from flet.core.gesture_detector import GestureDetector
from datetime import date
from day_view import day_view
from calendar_view import calendar_view
from typing import Callable, cast
import flet as ft

import components
from dateutil.relativedelta import relativedelta
import utils


class gui:
    _calendar: calendar_view
    _current_date: date = date.today()
    _day_view: day_view
    _slider: GestureDetector
    _page: ft.Page

    def move_vertical_divider(self, e: ft.DragUpdateEvent):
        """Called when the vertical divider is moved

        Args:
            e (ft.DragUpdateEvent): Event that has information about the mouse movement
        """
        min_width, max_width = 200, 1000
        if e.delta_x > 0 and self._day_view.width and self._day_view.width < max_width:
            self._day_view.width = min(self._day_view.width + e.delta_x, max_width)
        elif (
            e.delta_x < 0 and self._day_view.width and self._day_view.width > min_width
        ):
            self._day_view.width = max(self._day_view.width + e.delta_x, min_width)
        self._day_view.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        """Change the cursor to a resize cursor on a hover event

        Args:
            e (ft.HoverEvent): A hover event
        """
        cast(
            ft.GestureDetector, e.control
        ).mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        cast(ft.GestureDetector, e.control).update()

    def on_day_click(self, clickedDay: int):
        """Change the event display to list events from a given day index

        Args:
            clickedDay (int): The index of the day of the month
        """
        if clickedDay != 0:
            # Relativedelta(day=[num]) sets the day instead of adds it. To add days it would be days instead of day
            self._day_view.refresh_event_list(
                self._current_date + relativedelta(day=clickedDay)
            )

    def open_date_picker_from_month(self, event: ft.ControlEvent):
        """Display a date picker

        Args:
            event (ft.ControlEvent): A button click event
        """
        components.create_popup_month_picker(self._page, self._current_date)
        cast(Callable[[], None], self._page.update)()

    def refresh(self):
        """Refresh the calendar view"""
        self._page.update() # pyright: ignore[reportUnknownMemberType]

    def __init__(self, page: ft.Page):
        self._page = page
        self._calendar = calendar_view(
            self._current_date + relativedelta(day=1),
            utils.get_last_date_in_month(self._current_date),
            self.on_day_click,
        )
        self._day_view = day_view(date.today())
        self._slider = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=self.move_vertical_divider,
            on_hover=self.show_draggable_cursor,
        )
        self._page.controls=[
            ft.Row(controls=[self._day_view,self._slider,self._calendar])
            ]
