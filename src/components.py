from datetime import date
from typing import Callable, cast
import flet

def create_popup_month_picker(page: flet.Page, current_date: date):
    row = flet.Row(
        controls=[
            flet.Text("Test"),
            flet.IconButton(
                flet.Icons.CLOSE,
                flet.Colors.ON_SURFACE_VARIANT,
                on_click=delete_popup_month_picker)
        ],
        alignment=flet.MainAxisAlignment.CENTER
    )
    container = flet.Container(
        content=row,
        bgcolor=flet.Colors.SURFACE_CONTAINER_HIGHEST,
        expand=True,
        alignment=flet.alignment.center,
        expand_loose=True
    )
    page.overlay.append(container)


def delete_popup_month_picker(event: flet.ControlEvent):
    cast(flet.Page, event.page).overlay.clear()
    cast(Callable[[], None],  cast(flet.Page, event.page).update)()
