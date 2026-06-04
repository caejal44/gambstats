from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, model_validator


class CreateSessionRequest(BaseModel):
    started_at: datetime = Field(...)
    casino: str = Field(...)
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.ended_at is not None and self.started_at is not None:
            if self.ended_at < self.started_at:
                raise ValueError("ended_at cannot be before started_at")
        return self

class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    trip_id: str
    casino: str
    started_at: str
    ended_at: Optional[str]
    created_at: str
    status: str
    notes: Optional[str]

class SessionListResponse(BaseModel):
    sessions: List[SessionResponse]

class UpdateSessionRequest(BaseModel):
    casino: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.ended_at is not None and self.started_at is not None:
            if self.ended_at < self.started_at:
                raise ValueError("ended_at cannot be before started_at")
        return self
