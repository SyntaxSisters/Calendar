from datetime import datetime, timedelta, date, time
import pickle
from typing import Any
import uuid
import flet as ft
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