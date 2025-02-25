from datetime import datetime, timedelta
from typing import Any, Optional
import uuid

class repeating_event:
    count: int | None
    exceptions:list[datetime] | None
    attachments: None

class calendar_event:
    start: datetime
    duration: timedelta
    tags:list[str]
    title:str
    location: dict[str, type[float]] = {
        'latitude':float,
        'longitude':float
    }
    repeating:repeating_event
    id:uuid.UUID
    def __init__(self):
        self.start = datetime.now()
        self.duration = timedelta(hours=1)
        self.tags = []
        self.title = "Untitled Event"
        self.id = uuid.uuid4()