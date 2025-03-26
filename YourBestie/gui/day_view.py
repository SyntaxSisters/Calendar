from datetime import date
import flet as ft
import calendar
from database import event

class day_view(ft.Container):
    event_list: ft.Column = ft.Column()
    day_label: ft.Text
    day: date

    def __init__(self, day: date, on_calendar_refresh: callable = None):
        """
        day: The currently displayed day
        on_calendar_refresh: A callback to refresh the calendar after deleting an event
        """
        super().__init__()
        self.day = day
        self._on_calendar_refresh = on_calendar_refresh

        self.day_label = ft.Text(
            value=f"{calendar.month_name[day.month]} {day.day}, {day.year}"
        )
        self.content: ft.Control = ft.Column(
            controls=[
                ft.Text(value="Day Selected", size=20, color=ft.Colors.ON_SURFACE),
                self.day_label,
                self.event_list,
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Add Event",
                            on_click=lambda e: self.open_create_event_popup(e)
                        )
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def select_day(self, new_day: date):
        self.day = new_day
        self.day_label.value = f"{calendar.month_name[new_day.month]} {new_day.day}, {new_day.year}"
        self.refresh_event_list(self.day)
        self.update()

    def open_create_event_popup(self, e):
        selected_date = self.day
        event.calendar_events.show_create_event_popup(
            e,
            selected_date,
            lambda: self.refresh_event_list(selected_date)
        )

    def refresh_event_list(self, day: date):
        self.event_list.controls.clear()
        self.day_label.value = f"{calendar.month_name[day.month]} {day.day}, {day.year}"

        events = event.calendar_events.get_events_for_day(day)

        if events:
            for ev in events:
                # show text and color circle
                event_text = ft.Text(f"{ev.title} - {ev.start_time} to {ev.end_time}")
                color_circle = ft.Container(width=12, height=12, border_radius=6, bgcolor=ev.color)

                # "View" icon
                view_btn = ft.IconButton(
                    icon=ft.Icons.REMOVE_RED_EYE,
                    tooltip="View event",
                    on_click=lambda _, ev_obj=ev: self.view_event(_, ev_obj)
                )

                # "Delete" button (X icon)
                delete_btn = ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    tooltip="Delete event",
                    on_click=lambda _, ev_obj=ev: self.remove_event(ev_obj)
                )

                row = ft.Row(
                    controls=[event_text, color_circle, view_btn, delete_btn],
                    spacing=8
                )
                self.event_list.controls.append(row)
                self.event_list.controls.append(
                    ft.Text(ev.pdf_summary, size=12, color=ft.Colors.ON_SURFACE_VARIANT)
                )
        else:
            self.event_list.controls.append(
                ft.Text("No events yet.", color=ft.Colors.ON_SURFACE)
            )

        self.update()

    def view_event(self, e, ev_obj):
        """Open the read-only 'View Event' popup."""
        event.calendar_events.show_view_event_popup(e, ev_obj)

    def remove_event(self, ev_obj):
        """Delete the event, then refresh both the Day View and the Month View."""
        event_id = str(ev_obj.id)
        event.calendar_events.delete_event(event_id)

        
        self.refresh_event_list(self.day)

        if self._on_calendar_refresh:
            self._on_calendar_refresh()

        self.update()
