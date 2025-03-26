# day_widget.py
import flet as ft
from datetime import date
from typing import Any, Callable
from flet.core.types import ControlEvent

class day_widget(ft.Container):
    _day: date
    _in_range: bool
    _day_click_event: Callable[[date], Any] | None

    def __init__(
        self,
        day: date,
        in_range: bool = False,
        highlight: bool = False,
        day_click_event: Callable[[date], Any] | None = None,
        colors: list[str] = None
    ):
        super().__init__()
        self._day = day
        self._in_range = in_range
        self._day_click_event = day_click_event
        if colors is None:
            colors = []

        self.width = 80
        self.height = 80
        self.border = ft.border.all(color=ft.Colors.OUTLINE, width=1)
        self.border_radius = 15
        self.alignment = ft.alignment.center

        # dim if out-of-range
        text_opacity = 1.0 if self._in_range else 0.3

        # highlight if selected
        if highlight:
            self.bgcolor = ft.Colors.SECONDARY_CONTAINER

        # Show up to 3 color circles, then +N
        max_show = 3
        circle_containers = []
        for c in colors[:max_show]:
            circle_containers.append(
                ft.Container(width=12, height=12, border_radius=6, bgcolor=c)
            )
        extra_count = len(colors) - max_show
        if extra_count > 0:
            circle_containers.append(ft.Text(f"+{extra_count}", size=11))

        day_text = ft.Container(
            content=ft.Text(str(day.day), size=20, opacity=text_opacity),
            alignment=ft.alignment.center
        )
        circles_row = ft.Container(
            content=ft.Row(controls=circle_containers, spacing=4),
            alignment=ft.alignment.top_center,
            padding=ft.padding.only(top=4)
        )

        self.content = ft.Stack(
            controls=[
                circles_row,
                day_text,
            ]
        )

        self.on_click = self.day_clicked

    def day_clicked(self, _: ControlEvent):
        if self._day_click_event:
            self._day_click_event(self._day)
