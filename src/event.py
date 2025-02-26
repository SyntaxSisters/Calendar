from datetime import datetime, timedelta, date, time
from typing import Any
import uuid

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
    