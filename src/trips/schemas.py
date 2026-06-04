from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class CreateTripRequest(BaseModel):
    trip_name: str = Field(...)
    location: str = Field(...)
    trip_budget: float = Field(...)
    started_at: datetime = Field(...)
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator("trip_budget")
    @classmethod
    def trip_budget_validator(cls, trip_budget):
        if trip_budget < 0:
            raise ValueError("trip_budget cannot be negative")
        return trip_budget

    @model_validator(mode="after")
    def validate_dates(self):
        if self.ended_at is not None and self.started_at is not None:
            if self.ended_at < self.started_at:
                raise ValueError("ended_at cannot be before started_at")
        return self

class TripResponse(BaseModel):
    trip_id: str
    user_id: str
    trip_name: str
    location: str
    trip_budget: float
    started_at: str
    ended_at: Optional[str]
    created_at: str
    status: str
    notes: Optional[str]

class TripListResponse(BaseModel):
    trips: List[TripResponse]

class UpdateTripRequest(BaseModel):
    trip_name: Optional[str] = None
    location: Optional[str] = None
    trip_budget: Optional[float] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None

    @field_validator("trip_budget")
    @classmethod
    def trip_budget_validator(cls, trip_budget):
        if trip_budget is not None and trip_budget < 0:
            raise ValueError("trip_budget cannot be negative")
        return trip_budget

    @model_validator(mode="after")
    def validate_dates(self):
        if self.ended_at is not None and self.started_at is not None:
            if self.ended_at < self.started_at:
                raise ValueError("ended_at cannot be before started_at")
        return self