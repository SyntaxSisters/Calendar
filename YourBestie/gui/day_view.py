from datetime import date
import flet as ft
import calendar
from database import event

class day_view(ft.Container):
    def __init__(self, day: date, on_calendar_refresh: callable = None, team: str = "Admin"):
        super().__init__()
        self.day = day
        self._team = team
        self._on_calendar_refresh = on_calendar_refresh

        # show selected day
        self.day_label = ft.Text(
            value=f"{calendar.month_name[day.month]} {day.day}, {day.year}"
        )

        # A ListView for the events - it scrolls automatically
        # had to add it cuz if u had too many events theyd go off the screen
        self.event_list_view = ft.ListView(
            spacing=10,
            padding=10,
            height=300,  # Example fixed height
            # expand=True
        )

        # Only Admin sees an "Add Event" button
        add_event_button_row = None
        if self._team.lower() == "admin":
            add_event_button_row = ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Add Event",
                        on_click=self.open_create_event_popup
                    )
                ],
                spacing=10
            )

        # buildjng a column of controls
        # (title text, day label, the ListView, and if allowed  the "Add Event"  + delete button)
        controls_list = [
            ft.Text("Day Selected", size=20, color=ft.Colors.ON_SURFACE),
            self.day_label,
            self.event_list_view
        ]
        if add_event_button_row:
            controls_list.append(add_event_button_row)

        self.content = ft.Column(
            controls=controls_list,
            alignment=ft.MainAxisAlignment.START,
        )

    def select_day(self, new_day: date):
        self.day = new_day
        self.day_label.value = f"{calendar.month_name[new_day.month]} {new_day.day}, {new_day.year}"
        self.refresh_event_list(new_day)
        self.update()

    def open_create_event_popup(self, e):
        selected_date = self.day

        def after_create_callback():
            self.refresh_event_list(selected_date)
            #  refresh the calendar so the badge is updated
            if self._on_calendar_refresh:
                self._on_calendar_refresh()

        # Only Admin can call this
        event.calendar_events.show_create_event_popup(
            e,
            selected_date,
            after_create_callback
        )

    def refresh_event_list(self, day: date):
        # Clear the old items
        self.event_list_view.controls.clear()
        self.day_label.value = f"{calendar.month_name[day.month]} {day.day}, {day.year}"

        # show filtered events
        events_for_day = event.calendar_events.get_events_for_day(day, self._team)

        if events_for_day:
            for ev in events_for_day:
                event_text = ft.Text(f"{ev.title} - {ev.start_time} to {ev.end_time}")
                color_circle = ft.Container(width=12, height=12, border_radius=6, bgcolor=ev.color)

                # everyone sees a "View" icon 
                view_btn = ft.IconButton(
                    icon=ft.Icons.VISIBILITY,
                    tooltip="View event details",
                    on_click=lambda _, ev_obj=ev: event.calendar_events.show_view_event_popup(_, ev_obj)
                )

                row_controls = [event_text, color_circle, view_btn]

                # Only Admin sees the delete icon
                if self._team.lower() == "admin":
                    delete_btn = ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        tooltip="Delete event",
                        on_click=lambda _, ev_obj=ev: self.remove_event(ev_obj)
                    )
                    row_controls.append(delete_btn)

                row = ft.Row(controls=row_controls, spacing=8)
                self.event_list_view.controls.append(row)

                self.event_list_view.controls.append(
                    ft.Text(ev.pdf_summary, size=12, color=ft.Colors.ON_SURFACE_VARIANT)
                )
        else:
            self.event_list_view.controls.append(
                ft.Text("No events yet.", color=ft.Colors.ON_SURFACE)
            )

        self.update()

    def remove_event(self, ev_obj):
        event_id = str(ev_obj.id)
        event.calendar_events.delete_event(event_id)
        self.refresh_event_list(self.day)

        #  refresh month badges
        if self._on_calendar_refresh:
            self._on_calendar_refresh()

        self.update()
