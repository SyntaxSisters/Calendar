from datetime import date
from typing import Callable, cast
import flet as ft
import calendar
import components
from dateutil.relativedelta import relativedelta

# main function

def main(page:ft.Page):

    # just for base
    
    current_date: date = date.today()
    selected_day = ft.Text("", size=18, color=ft.Colors.ON_SURFACE)
    event_list = ft.Column()

    # hide the event input form at start
    event_form = ft.Column(visible=False)
    # error message for date selection
    date_error = ft.Text("", color=ft.Colors.ON_ERROR, size=14)

    def refresh_event_list(day:date):
        event_list.controls.clear()
        selected_day.value = f"{calendar.month_name[day.month]} {day.day}, {day.year}"
        event_list.controls.append(ft.Text("No events yet.", color=ft.Colors.ON_SURFACE))
        cast(Callable[[],None],page.update)()

    # show the event input form
    def add_event(event:ft.ControlEvent):
        if not selected_day.value:  # check if a date is selected
            date_error.value = "Please select a date first."
            cast(Callable[[],None],page.update)()
        else:
            date_error.value = ""  # clear the error message
            event_form.visible = True  # mke the event form visible if a date is selected
            cast(Callable[[],None],page.update)()

    # cancel event input form
    def cancel_event(event:ft.ControlEvent):
        event_form.visible = False  # hide the event form
        cast(Callable[[],None],page.update)()

    
    dayEvents = ft.Container(
        content=ft.Column(
            [
                ft.Text("Day Selected", size=20,
                        color=ft.Colors.ON_SURFACE), selected_day, event_list,
                ft.Row([
                    ft.ElevatedButton(
                        "Add Event", on_click=add_event),
                    ft.ElevatedButton(
                        "Cancel", on_click=cancel_event)
                ], spacing=10),
                date_error,  # Show the error message here
                event_form  # Add the event form
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        height=page.height,
        width=400,
        bgcolor=ft.Colors.SURFACE,
        padding=20,
        border_radius=10
    )

    def move_vertical_divider(e: ft.DragUpdateEvent):
        min_width,max_width=200,1000
        if (e.delta_x > 0 and dayEvents.width and dayEvents.width < max_width):
            dayEvents.width = min(dayEvents.width + e.delta_x,max_width)
        elif(e.delta_x < 0 and dayEvents.width and dayEvents.width > min_width):
            dayEvents.width = max(dayEvents.width + e.delta_x,min_width)
        dayEvents.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        cast(ft.GestureDetector,e.control).mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        cast(ft.GestureDetector,e.control).update()

    # switching through months
    def update_calendar():
        page.controls.clear()

        cal = components.create_calendar(
            current_date.replace(day=1), current_date.replace(day=calendar.monthrange(current_date.year,current_date.month)[1]), on_day_click)
        slider = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=move_vertical_divider,
            on_hover=show_draggable_cursor
        )
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(
                        ft.Icons.ARROW_LEFT, on_click=prev_month, tooltip="Previous Month", width=40),
                    ft.TextButton(
                        f"{calendar.month_name[current_date.month]} {current_date.year}", on_click=open_date_picker_from_month),
                    ft.IconButton(
                        ft.Icons.ARROW_RIGHT, on_click=next_month, tooltip="Next Month", width=40),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    dayEvents, slider, cal
                ],expand=True)
            ],expand=True)
        )

        # Event input form
        title_input = ft.TextField(
            label="Event Title", width=250)
        location_input = ft.TextField(
            label="Location", width=250)
        description_input = ft.TextField(
            label="Description", width=250)
        start_time_input = ft.TextField(
            label="Start Time", width=250)
        end_time_input = ft.TextField(
            label="End Time", width=250)
            
        # submit the event (nothing saved for now but later it will)
        def submit_event(event:ft.ControlEvent):
            title = title_input.value
            location = location_input.value
            description = description_input.value
            start_time = start_time_input.value
            end_time = end_time_input.value

            print(
                f"Event Added: {title}, {location}, {description}, {start_time}, {end_time}")

            # hide the form after submission
            event_form.visible = False
            cast(Callable[[],None],page.update)()

        event_form.controls = [
            title_input, location_input, description_input, start_time_input, end_time_input,
            ft.ElevatedButton("Submit Event", on_click=submit_event)
        ]
        cast(Callable[[],None],page.update)()

    # change the month
    def prev_month(event:ft.ControlEvent):
        nonlocal current_date
        current_date = current_date - relativedelta(months=1)
        update_calendar()

    def next_month(event:ft.ControlEvent):
        nonlocal current_date
        current_date = current_date + relativedelta(months=1)
        update_calendar()

    def on_day_click(clickedDay:int):
        if clickedDay != 0:
            refresh_event_list(current_date + relativedelta(day=clickedDay))

    # TODO open a date picker when the user clicks on the month title
    def open_date_picker_from_month(event:ft.ControlEvent):
       components.create_popup_month_picker(cast(ft.Page,event.page), current_date)
       cast(Callable[[],None],page.update)()
       
    update_calendar()


# work app pls don't crash..
_ = cast(Callable[[Callable[[ft.Page],None]],None],ft.app)(main)