import calendar
from typing import Callable
import flet
def create_calendar(year:int, month:int, on_day_click:Callable[[int],None]):
    cell_width = 80
    cal = calendar.monthcalendar(year, month)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header = flet.Container(flet.Row(
        [flet.Text(day, size=24, width=cell_width, text_align=flet.TextAlign.CENTER, color=flet.Colors.ON_PRIMARY)
            for day in weekdays],
    ),bgcolor=flet.Colors.PRIMARY)
    
    days_grid:list[flet.Control] = []
    for week in cal:
        days_grid.append(
            flet.Row([
                flet.Container(
                    content=flet.Text(str(day) if day != 0 else "", size=24,
                                    color=flet.Colors.ON_PRIMARY_CONTAINER),
                    width=cell_width,
                    height=cell_width,
                    bgcolor=flet.Colors.PRIMARY_CONTAINER if day != 0 else "transparent",
                    border_radius=5,
                    border=flet.border.all(1, "white"),
                    alignment=flet.alignment.center,
                    on_click=lambda e, d=day: on_day_click(
                        d) if d != 0 else None
                )
                for day in week
            ])
        )
    columns = flet.Column(controls=[header]+days_grid)
    container = flet.Container(columns,bgcolor=flet.Colors.SURFACE,expand=1)
    return container