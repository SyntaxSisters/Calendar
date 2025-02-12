import flet as ft
import calendar
from datetime import datetime

# creating calendar for year and month
def create_calendar(year, month, on_day_click):
    cal = calendar.monthcalendar(year, month)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    header = ft.Row(
        [ft.Text(day, size=24, width=60, text_align=ft.TextAlign.CENTER, color="white", bgcolor="lightgrey") 
            for day in weekdays]
    )

    days_grid = []
    for week in cal:
        days_grid.append(
            ft.Row([ 
                ft.Container(
                    content=ft.Text(str(day) if day != 0 else "", size=24, width=60, text_align=ft.TextAlign.CENTER, color="white"),
                    width=60,
                    height=60,
                    bgcolor="black" if day != 0 else "transparent",
                    border_radius=5,
                    border=ft.border.all(1, "white"),
                    alignment=ft.alignment.center,
                    on_click=lambda e, d=day: on_day_click(d) if d != 0 else None
                ) 
                for day in week
            ])
        )

    return header, days_grid

# main function
def main(page):

    # just for base
    current_year = 2025
    current_month = 2

    selected_day = ft.Text("", size=18, color="white")
    event_input = ft.TextField(label="Add Event", width=250)
    event_list = ft.Column()

    # hide the event input form at start
    event_form = ft.Column(visible=False)  
    date_error = ft.Text("", color="red", size=14)  # error message for date selection

    def refresh_event_list(day):
        event_list.controls.clear()
        selected_day.value = f"{calendar.month_name[current_month]} {day}, {current_year}"
        event_list.controls.append(ft.Text("No events yet.", color="white"))
        page.update()

    # show the event input form
    def add_event(e):
        if not selected_day.value:  # check if a date is selected
            date_error.value = "Please select a date first."
            page.update()
        else:
            date_error.value = ""  # clear the error message
            event_form.visible = True  # mke the event form visible if a date is selected
            page.update()

    # cancel event input form
    def cancel_event(e):
        event_form.visible = False  # hide the event form
        page.update()

    # submit the event (nothing saved for now but later it will)
    def submit_event(e):
        title = title_input.value
        location = location_input.value
        description = description_input.value
        start_time = start_time_input.value
        end_time = end_time_input.value

        print(f"Event Added: {title}, {location}, {description}, {start_time}, {end_time}")

        # hide the form after submission
        event_form.visible = False
        page.update()

    # switching through months
    def update_calendar():
        page.controls.clear()

        header, days_grid = create_calendar(current_year, current_month, on_day_click)

        calendar_column = ft.Column(
            [header] + days_grid, alignment=ft.MainAxisAlignment.START
        )

        page.add(
            ft.Stack([
                ft.Container(
                    image_src="backgroundtemp.png",  # WHY ISN'T THIS WORKING IDK BUT I'LL FIX IT 
                    image_fit=ft.ImageFit.FILL,
                    expand=True
                ),
                ft.Column([
                    ft.Text("Syntax Sisters", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="white"),
                    ft.Row([
                        ft.IconButton(ft.icons.ARROW_LEFT, on_click=prev_month, tooltip="Previous Month", width=40),
                        ft.Text(f"{calendar.month_name[current_month]} {current_year}", size=18, color="white"),
                        ft.IconButton(ft.icons.ARROW_RIGHT, on_click=next_month, tooltip="Next Month", width=40),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                        # Left column
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Day Selected", size=20, color="white"), selected_day, event_list,
                                    ft.Row([
                                        ft.ElevatedButton("Add Event", on_click=add_event),
                                        ft.ElevatedButton("Cancel", on_click=cancel_event)
                                    ], spacing=10),
                                    date_error,  # Show the error message here
                                    event_form  # Add the event form 
                                ], 
                                alignment=ft.MainAxisAlignment.START
                            ),
                            width=page.width * 0.3,
                            height=page.height,
                            bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
                            padding=20,
                            border_radius=10
                        ),  
                        # Right column (Calendar)
                        ft.Container(
                            content=calendar_column,
                            width=page.width * 0.66,
                            height=page.height,
                            padding=20,
                            bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
                            border_radius=10
                        )
                    ], alignment=ft.MainAxisAlignment.START)
                ])
            ])
        )

        # Event input form
        title_input = ft.TextField(label="Event Title", width=250, border=ft.border.all(2, "white"))
        location_input = ft.TextField(label="Location", width=250, border=ft.border.all(2, "white"))
        description_input = ft.TextField(label="Description", width=250, border=ft.border.all(2, "white"))
        start_time_input = ft.TextField(label="Start Time", width=250, border=ft.border.all(2, "white"))
        end_time_input = ft.TextField(label="End Time", width=250, border=ft.border.all(2, "white"))

        event_form.controls = [
            title_input, location_input, description_input, start_time_input, end_time_input,
            ft.ElevatedButton("Submit Event", on_click=submit_event)
        ]

        page.update()

    # change the month
    def prev_month(e):
        nonlocal current_month, current_year
        if current_month == 1:
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
        update_calendar()

    def next_month(e):
        nonlocal current_month, current_year
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1
        update_calendar()

    def on_day_click(day):
        if day != 0:
            refresh_event_list(day)

    update_calendar()

# work app pls don't crash..
ft.app(target=main)
