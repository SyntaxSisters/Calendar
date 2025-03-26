import flet as ft
from datetime import date
from typing import Any, Callable
from flet.core.types import ControlEvent

def chunk_list(lst, chunk_size):
    """Helper to split a list into sub-lists of a given size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]

class day_widget(ft.Container):
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
        self.width = 80
        self.height = 80
        self.border = ft.border.all(color=ft.Colors.OUTLINE, width=1)
        self.border_radius = 15
        self.on_click = self.day_clicked
        self.on_hover = self.handle_hover  # hover trigger

        if colors is None:
            colors = []

        # dim the text if this day is out-of-range.
        text_opacity = 1.0 if self._in_range else 0.3

        # highlight if selected.
        if highlight:
            self.bgcolor = ft.Colors.SECONDARY_CONTAINER

        # Limited row when not hovered =  3 circles +  "+N"
        max_show = 3
        limited_controls = []
        for c in colors[:max_show]:
            limited_controls.append(
                ft.Container(width=12, height=12, border_radius=6, bgcolor=c)
            )
        extra_count = len(colors) - max_show
        if extra_count > 0:
            limited_controls.append(ft.Text(f"+{extra_count}", size=11))

        self.limited_row = ft.Row(
            controls=limited_controls,
            spacing=4,
            visible=True  
        )

        # "Full" view when hovered:  circles in rows of 5
        all_rows = []
        for chunk in chunk_list(colors, 5):
            row_controls = []
            for c in chunk:
                row_controls.append(
                    ft.Container(width=12, height=12, border_radius=6, bgcolor=c)
                )
            all_rows.append(ft.Row(controls=row_controls, spacing=4))

        self.all_circles_column = ft.Column(
            controls=all_rows,
            spacing=4,
            visible=False 
        )

        # moved day number at the bottom for teh badges

        day_label = ft.Text(str(day.day), size=20, opacity=text_opacity)


        #build
        self.content_column = ft.Column(
            width=80,
            height=80,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # At the top,  keep both sets of badges, toggling visibility on hover
                ft.Column(
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.limited_row,
                        self.all_circles_column,
                    ],
                ),
                # The day label near the bottom
                day_label,
            ],
        )

        self.content = self.content_column

    def day_clicked(self, _: ControlEvent):
        """When the user clicks this day, call the callback if provided."""
        if self._day_click_event:
            self._day_click_event(self._day)

    def handle_hover(self, e: ft.HoverEvent):
        """
        On hover, hide the "limited" row and show the "full" circles.
        On hover-out, restore the limited row.
        """
        hovering = (e.data == "true")
        self.limited_row.visible = not hovering
        self.all_circles_column.visible = hovering
        self.content_column.update()
