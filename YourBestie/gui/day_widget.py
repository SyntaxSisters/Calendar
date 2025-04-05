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
        colors: list[str] = None,
    ):
        super().__init__()
        self._day = day
        self._in_range = in_range
        self._day_click_event = day_click_event
        self.width = 100
        self.height = 100
        self.border_radius = 15
        self.on_click = self.day_clicked
        self.on_hover = self.handle_hover  # hover trigger
        self.animate = ft.Animation(200, "easeInOut") # fancy animation

        if colors is None:
            colors = []

        # highlight if selected
        if highlight:
            self.bgcolor = ft.Colors.SECONDARY_CONTAINER
        elif self._day == date.today():
            self.bgcolor = ft.colors.with_opacity(0.08, ft.colors.PRIMARY)
        elif not self._in_range:
            self.bgcolor = ft.colors.SURFACE_VARIANT
        else:
            self.bgcolor = ft.colors.SURFACE

        self.border = ft.border.all(color=ft.Colors.OUTLINE, width=1)

        # soft glow
        self.shadow = ft.BoxShadow(
            blur_radius=6, spread_radius=0, color=ft.colors.with_opacity(0.1, ft.colors.PRIMARY)
        )

        # dim the text if this day is out-of-range.
        text_opacity = 1.0 if self._in_range else 0.3
        
        # moved day number back to the top left and changed the badge wrapping
        day_label = ft.Text(str(day.day), size=14, weight=ft.FontWeight.BOLD, opacity=text_opacity)

        preview_dots = colors[:2]
        hidden_dots = colors[2:]

        # Limited row when not hovered =  2 circles +  "+N"
        preview_row_controls = [
            day_label
        ] + [
            ft.Container(
                width=10,
                height=10,
                bgcolor=c,
                border_radius=99,
                margin=ft.Margin(2, 0, 0, 0),
                shadow=ft.BoxShadow(blur_radius=1, color=ft.colors.with_opacity(0.15, c)),
                border=ft.border.all(1, ft.colors.with_opacity(0.2, ft.colors.BLACK)),
            )
            for c in preview_dots
        ]

        if len(hidden_dots) > 0:
            self.plus_more = ft.Text(f"+{len(hidden_dots)}", size=11, opacity=0.7)
            preview_row_controls.append(self.plus_more)
        else:
            self.plus_more = None

        self.preview_row = ft.Row(
            controls=preview_row_controls,
            alignment=ft.MainAxisAlignment.START,
            spacing=4,
            visible=True
        )

        # "Full" view:  circles in rows of 5
        all_dot_rows = []
        for chunk in chunk_list(colors, 5):
            row_controls = [
                ft.Container(
                    width=10,
                    height=10,
                    bgcolor=c,
                    border_radius=99,
                    shadow=ft.BoxShadow(blur_radius=1, color=ft.colors.with_opacity(0.15, c)),
                    border=ft.border.all(1, ft.colors.with_opacity(0.2, ft.colors.BLACK)),
                )
                for c in chunk
            ]
            all_dot_rows.append(ft.Row(controls=row_controls, spacing=4))

        self.full_view_column = ft.Column(
            controls=all_dot_rows,
            spacing=4,
            visible=False,
        )
        
        self.dot_column = ft.Column(
            controls=[self.preview_row, self.full_view_column],
            spacing=4,
        )

        #build
        self.content_column = ft.Column(
            width=100,
            height=100,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    content=self.dot_column,
                    padding=ft.Padding(6, 6, 6, 0),
                )
            ],
        )

        self.content = self.content_column

    def day_clicked(self, _: ControlEvent):
        """When the user clicks this day, call the callback if provided."""
        self.shadow = ft.BoxShadow(
            blur_radius=12,
            spread_radius=4,
            color=ft.colors.with_opacity(0.3, ft.colors.PRIMARY),
        )
        self.update()

        def reset_glow():
            self.shadow = ft.BoxShadow(
                blur_radius=6,
                spread_radius=1,
                color=ft.colors.with_opacity(0.15, ft.colors.PRIMARY),
            )
            self.update()

        import threading
        threading.Timer(0.2, reset_glow).start()

        if self._day_click_event:
            self._day_click_event(self._day)

    def handle_hover(self, e: ft.HoverEvent):
        """
        On hover, hide the "limited" row and show the "full" circles and applies a soft glowing shadow..
        On hover-out, restore the limited row.
        """
        hovering = (e.data == "true")

        # if there are event dots, toggle them
        if hasattr(self, "preview_row") and hasattr(self, "full_view_column"):
            self.preview_row.visible = not hovering
            self.full_view_column.visible = hovering
            if self.plus_more:
                self.plus_more.visible = not hovering
            self.dot_column.update()

        # hover shadow glow
        self.shadow = (
            ft.BoxShadow(
                blur_radius=8,
                spread_radius=2,
                color=ft.colors.with_opacity(0.25, ft.colors.PRIMARY),
                offset=ft.Offset(0, 2),
            )
            if hovering
            else ft.BoxShadow(
                blur_radius=3,
                spread_radius=0,
                color=ft.colors.with_opacity(0.08, ft.colors.PRIMARY),
                offset=ft.Offset(0, 1),
            )
        )

        self.update()


