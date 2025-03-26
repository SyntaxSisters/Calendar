# window.py
from flet.core.gesture_detector import GestureDetector
from datetime import date
from .day_view import day_view
from .calendar_view import calendar_view
from typing import cast
import flet as ft

class gui:
    _calendar: calendar_view
    _current_date: date = date.today()
    _day_view: day_view
    _slider: GestureDetector
    _page: ft.Page

    def __init__(self, page: ft.Page):
        self._page = page
        self._calendar = calendar_view(self._current_date, self.on_day_click)
        self._calendar.expand = False
        self._calendar.adaptive = False

        self._day_view = day_view(date.today(), on_calendar_refresh=self.refresh_calendar)
        self._day_view.expand = True

        self._slider = ft.GestureDetector(
            content=ft.VerticalDivider(visible=True),
            drag_interval=10,
            on_pan_update=self.move_vertical_divider,
            on_hover=self.show_draggable_cursor,
        )

        self._page.controls = [
            ft.Row(controls=[self._day_view, self._slider, self._calendar])
        ]

    def on_day_click(self, clicked_day: date):
        """Update the selected date in day_view and refresh."""
        self._current_date = clicked_day
        self._day_view.select_day(clicked_day)
        self._calendar.update()
        self._page.update()

    def refresh_calendar(self):
        """Rebuild the calendar to update the color circles."""
        self._calendar.build()
        self._calendar.update()
        self._page.update()

    def move_vertical_divider(self, e: ft.DragUpdateEvent):
        min_width, max_width = 200, 1000
        if e.delta_x > 0 and self._day_view.width and self._day_view.width < max_width:
            self._day_view.width = min(self._day_view.width + e.delta_x, max_width)
        elif (
            e.delta_x < 0 and self._day_view.width and self._day_view.width > min_width
        ):
            self._day_view.width = max(self._day_view.width + e.delta_x, min_width)
        self._day_view.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        cast(ft.GestureDetector, e.control).mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        cast(ft.GestureDetector, e.control).update()

    def refresh(self):
        self._slider = ft.GestureDetector(
            content=ft.VerticalDivider(visible=True),
            drag_interval=10,
            on_pan_update=self.move_vertical_divider,
            on_hover=self.show_draggable_cursor,
        )
        self._page.controls.clear()
        self._page.controls = [
            ft.Row(controls=[self._day_view, self._slider, self._calendar])
        ]
        self._page.update()
