from datetime import date
from typing import Any, Callable
import flet as ft
from flet.core.types import ControlEvent
class day_widget(ft.Container):
    _day:date
    _in_range:bool
    _day_click_event:Callable[[date], Any] | None
    def __init__(self, day:date, in_range:bool = False, highlight:bool = False, day_click_event:Callable[[date], Any] | None = None, event_count:int = 0):
        super().__init__() # pyright: ignore[reportUnknownMemberType]
        self._day = day
        self._in_range = in_range
        self._day_click_event = day_click_event
        opacity = 1 if self._in_range else 0.3
        self.content:ft.Control=ft.Text(
                        value=f"{self._day.day}",
                        size=24,
                        opacity=opacity
                    )
        self.border_radius:int=5
        if event_count != 0:
            self.badge:ft.Badge = ft.Badge(text=str(event_count))
        self.alignment:ft.Alignment=ft.alignment.center
        self.on_click:Callable[[ft.ControlEvent],None] = self.day_clicked
    
    def day_clicked(self, _: ControlEvent):
        if self._day_click_event is not None:
            self._day_click_event(self._day)