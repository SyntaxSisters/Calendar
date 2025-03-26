from flet.core.gesture_detector import GestureDetector
from datetime import date
from .day_view import day_view
from .calendar_view import calendar_view
from typing import cast
import flet as ft

class gui:
    _current_date: date = date.today()
    
    def __init__(self, page: ft.Page, team: str):
        self._team = team
        self._page = page
        # Pass the team to both the calendar and day views.
        self._calendar = calendar_view(self._current_date, self.on_day_click, team=self._team)
        self._calendar.expand = False
        self._calendar.adaptive = False

        self._day_view = day_view(date.today(), on_calendar_refresh=self.refresh_calendar, team=self._team)
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
        self._current_date = clicked_day
        self._day_view.select_day(clicked_day)
        self._calendar.update()
        self._page.update()

    def refresh_calendar(self):
        self._calendar.build()
        self._calendar.update()
        self._page.update()

    def move_vertical_divider(self, e: ft.DragUpdateEvent):
        min_width, max_width = 200, 1000
        if e.delta_x > 0 and self._day_view.width and self._day_view.width < max_width:
            self._day_view.width = min(self._day_view.width + e.delta_x, max_width)
        elif e.delta_x < 0 and self._day_view.width and self._day_view.width > min_width:
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
