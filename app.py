from datetime import date
from typing import Callable, cast
import flet as ft
import calendar
import components
from dateutil.relativedelta import relativedelta


class CalendarApp:

    def __init__(self, page: ft.Page):
        self.page = page
        self.current_date = date.today()
        self.selected_day = ft.Text("", size=18, color=ft.Colors.ON_SURFACE)
        self.event_list = ft.Column()
        self.event_form = ft.Column(visible=False)
        self.date_error = ft.Text("", color=ft.Colors.ON_ERROR, size=14)

        self.initialize_ui()

    def initialize_ui(self):
        self.day_events = ft.Container(
            content=ft.Column([
                ft.Text("Day Selected", size=20, color=ft.Colors.ON_SURFACE),
                self.selected_day,
                self.event_list,
                ft.Row([
                    ft.ElevatedButton("Add Event", on_click=self.add_event),
                    ft.ElevatedButton("Cancel", on_click=self.cancel_event)
                ], spacing=10),
                self.date_error,
                self.event_form
            ], alignment=ft.MainAxisAlignment.START),
            height=self.page.height,
            width=400,
            bgcolor=ft.Colors.SURFACE,
            padding=20,
            border_radius=10
        )

        self.update_calendar()

    def refresh_event_list(self, day: date):
        self.event_list.controls.clear()
        self.selected_day.value = f"{calendar.month_name[day.month]} {day.day}, {day.year}"
        self.event_list.controls.append(ft.Text("No events yet.", color=ft.Colors.ON_SURFACE))
        self.page.update()

    def add_event(self, event: ft.ControlEvent):
        if not self.selected_day.value:
            self.date_error.value = "Please select a date first."
            self.page.update()
        else:
            self.date_error.value = ""
            self.event_form.visible = True
            self.page.update()

    def cancel_event(self, event: ft.ControlEvent):
        self.event_form.visible = False
        self.page.update()

    def submit_event(self, event: ft.ControlEvent):
        title = self.event_form.controls[0].value
        location = self.event_form.controls[1].value
        description = self.event_form.controls[2].value
        start_time = self.event_form.controls[3].value
        end_time = self.event_form.controls[4].value

        print(f"Event Added: {title}, {location}, {description}, {start_time}, {end_time}")
        self.event_form.visible = False
        self.page.update()

    def update_calendar(self):
        self.page.controls.clear()

        cal = components.create_calendar(
            self.current_date.replace(day=1),
            self.current_date.replace(day=calendar.monthrange(self.current_date.year, self.current_date.month)[1]),
            self.on_day_click
        )

        slider = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=self.move_vertical_divider,
            on_hover=self.show_draggable_cursor
        )

        self.page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.Icons.ARROW_LEFT, on_click=self.prev_month, tooltip="Previous Month", width=40),
                    ft.TextButton(f"{calendar.month_name[self.current_date.month]} {self.current_date.year}", on_click=self.open_date_picker_from_month),
                    ft.IconButton(ft.Icons.ARROW_RIGHT, on_click=self.next_month, tooltip="Next Month", width=40),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    self.day_events, slider, cal
                ], expand=True)
            ], expand=True)
        )

        self.event_form.controls = [
            ft.TextField(label="Event Title", width=250),
            ft.TextField(label="Location", width=250),
            ft.TextField(label="Description", width=250),
            ft.TextField(label="Start Time", width=250),
            ft.TextField(label="End Time", width=250),
            ft.ElevatedButton("Submit Event", on_click=self.submit_event)
        ]
        self.page.update()

    def move_vertical_divider(self, e: ft.DragUpdateEvent):
        min_width, max_width = 200, 1000
        if e.delta_x > 0 and self.day_events.width < max_width:
            self.day_events.width = min(self.day_events.width + e.delta_x, max_width)
        elif e.delta_x < 0 and self.day_events.width > min_width:
            self.day_events.width = max(self.day_events.width + e.delta_x, min_width)
        self.day_events.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        cast(ft.GestureDetector, e.control).mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        cast(ft.GestureDetector, e.control).update()

    def on_day_click(self, clicked_day: int):
        if clicked_day != 0:
            self.refresh_event_list(self.current_date + relativedelta(day=clicked_day))

    def prev_month(self, event: ft.ControlEvent):
        self.current_date = self.current_date - relativedelta(months=1)
        self.update_calendar()

    def next_month(self, event: ft.ControlEvent):
        self.current_date = self.current_date + relativedelta(months=1)
        self.update_calendar()

    def open_date_picker_from_month(self, event: ft.ControlEvent):
        components.create_popup_month_picker(cast(ft.Page, event.page), self.current_date)
        self.page.update()


def main(page: ft.Page):
    app = CalendarApp(page)


# Launch the app
_ = cast(Callable[[Callable[[ft.Page], None]], None], ft.app)(main)
