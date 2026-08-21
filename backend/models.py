from pydantic import BaseModel
from datetime import datetime

class SecurityEvent(BaseModel):
    timestamp: datetime
    event_type: str
    username: str
    ip_address: str