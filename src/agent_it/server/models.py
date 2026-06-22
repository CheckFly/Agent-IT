from datetime import datetime
from pydantic import BaseModel


class ActivityEvent(BaseModel):
    source_application: str
    agent_version: str

    hostname: str
    computer_uuid: str

    ip_address: str

    event_id: int
    record_id: int

    event_timestamp: datetime