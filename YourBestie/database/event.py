from datetime import datetime, timedelta, date, time
import _pickle
import uuid
import flet as ft
from typing import Any
class calendar_event:
    start_date: date = date.today()
    start_time: time = datetime.now().time()
    duration: timedelta = timedelta(hours=1)
    tags:list[str] = []
    title:str = "Untitled Event"
    location: tuple[float,float] = (0,0)
    repetitions:int = 1
    id:uuid.UUID = uuid.uuid4()
    attachments:list[list[Any]] = []
    def __init__(self):
        pass

class calendar_events:

    events: list[calendar_event] = []

    @staticmethod
    def show_create_event_popup(e):
        
        start_date = ft.DatePicker(value=date.today())
        start_time = ft.TimePicker(value=datetime.now().time())
        duration = ft.TextField(value="1:00", label="Duration (HH:MM)")
        tags = ft.TextField(value="", label="Tags (comma-separated)")
        title = ft.TextField(value="", label="Title", hint_text="Enter a title for the event")
        location = (ft.TextField(value="", label="Latitude"), ft.TextField(value="", label="Longitude"))
        repetitions = ft.TextField(value="", label="Repetitions")
        id_value = uuid.uuid4()
        attachments = ft.TextField(value="", label="Attachments (URLs)")
        
        content=ft.Container(
            content=ft.Column(
                [
                    title,
                    start_date, 
                    start_time,
                    duration,
                    tags,
                    ft.Row(
                        [location[0],location[1]],
                        spacing=20
                    ),
                    repetitions,
                    attachments
                ],

                spacing=20,
                alignment=ft.MainAxisAlignment.START

            ),
            padding=20,
            alignment=ft.alignment.top_left,
            width=800,
            height=500,
        )

        dlg_model = ft.AlertDialog(
            title=ft.Text("Create Event"),
            content=content,

            actions=[
                ft.TextButton("Create Event", on_click=lambda e: print("Create Event")), #connect the save_event function here after it's done <3
                ft.TextButton("Cancel", on_click=lambda e: close_dialogue(e))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: close_dialogue(e),
        )

        def close_dialogue(e):
            dlg_model.open = False
            e.control.page.update()
        
        def open_dialogue(e):
            e.control.page.controls.append(dlg_model)
            dlg_model.open = True
            e.control.page.update()

        open_dialogue(e)

    @staticmethod
    def get_events_for_day(day: date) -> list[calendar_event]:
        """Retrieve events scheduled for a given day."""
        return [event for event in calendar_events.events if event.start_date == day]
    
    @staticmethod
    def save_events(filepath:str):
        with open(filepath, "wb") as file:
            pickle.dump(calendar_events.events,file)
    
    @staticmethod
    def load_events(filepath:str):
        with open(filepath, "rb") as file:
            calendar_events.events = pickle.load(file)