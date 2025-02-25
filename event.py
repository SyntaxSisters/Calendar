from datetime import datetime, timedelta, date, time
from typing import Any, Optional
import uuid

class calendar_event:
    start: datetime = datetime.now()
    duration: timedelta = timedelta(hours=1)
    tags:list[str] = []
    title:str
    location: dict[str, type[float]] = {
        'latitude':float,
        'longitude':float
    }
    repetitions:int = 1
    id:uuid.UUID = uuid.uuid4()
    attachments:list[list[Any]] = []
    def __init__(self):
        self.start = datetime.now()
        self.title = "Untitled Event"

class calendar_events:
    events:list[calendar_event] = []
    