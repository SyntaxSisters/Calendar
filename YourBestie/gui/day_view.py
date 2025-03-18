from datetime import date
import flet as ft
import calendar
from flet.core.types import BorderRadiusValue

from database import event

class day_view(ft.Container):
    event_list: ft.Column = ft.Column()
    event_form: ft.Column = ft.Column(visible=False)
    day_label: ft.Text
    day: date

    def __init__(self, day: date):
        super().__init__()  # pyright: ignore[reportUnknownMemberType]
        self.day = day
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
                            "Add Event", on_click=lambda e: event.calendar_events.show_create_event_popup(e)
                        )
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.bgcolor: "ft.Colors" = ft.Colors.SURFACE
        self.padding: ft.PaddingValue = 20
        self.border_radius: BorderRadiusValue = 10

    def refresh_event_list(self, day: date):
        """Clear and repopulate the event list for the selected day

        Args:
            day (date): A date to populate events for
        """
        self.event_list.controls.clear()
        self.day_label.value = f"{calendar.month_name[day.month]} {day.day}, {day.year}"
        
        events = calendar_events.get_events_for_day(day)
    
        if events:
            for ev in events:
                self.event_list.controls.append(ft.Text(f"{ev.title} - {ev.start_time.strftime('%H:%M')}"))
        else:
            self.event_list.controls.append(ft.Text("No events yet.", color=ft.Colors.ON_SURFACE))
        
        self.update()

