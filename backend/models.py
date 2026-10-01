from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SecurityEvent(BaseModel):
    timestamp: datetime
    event_type: str
    username: str
    ip_address: str
    port: Optional[int] = None