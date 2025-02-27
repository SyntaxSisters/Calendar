from datetime import datetime, timedelta, date, time
from typing import Any
import uuid
import flet as ft
class calendar_event:
    start_date: date = date.today()
    start_time: time = datetime.now().time()
    duration: timedelta = timedelta(hours=1)
    tags:list[str] = []
    title:str = "Untitled Event"
    location: dict[str, type[float]] = {
        'latitude':float,
        'longitude':float
    }
    repetitions:int = 1
    id:uuid.UUID = uuid.uuid4()
    attachments:list[list[Any]] = []
    def __init__(self):
        pass

class calendar_events:
    events:list[calendar_event] = []
    
    @staticmethod
    def show_create_event_popup(event: ft.ControlEvent) -> None:
        raise NotImplementedError("Event creation is not yet implemented!")

    @staticmethod
    def add_event(event: calendar_event) -> None:
        """Add an event to the calendar

        Args:
            event (ft.ControlEvent): A button click event
        """
        raise NotImplementedError("Event creation is not yet implemented!")