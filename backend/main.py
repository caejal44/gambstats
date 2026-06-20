from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.trips.service import create_trip as create_trip_service
from src.sessions.service import create_session as create_session_service

app = FastAPI()


class CreateTripRequest(BaseModel):
    trip_name: str
    location: str
    trip_budget: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    notes: str = ""

class CreateSessionRequest(BaseModel):
    casino: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    notes: str = ""

@app.post("/trips")
def create_trip_endpoint(payload: dict):
    user_id = "dev-user"

    request = CreateTripRequest(
    trip_name=payload["tripName"],
    location=payload["location"],
    trip_budget=payload["tripBudget"],
    started_at=datetime.fromisoformat(payload["startedAt"]),
    ended_at=None,
    notes=payload.get("notes", ""),
)

    return create_trip_service(request, user_id)

@app.post("/sessions")
def create_session_endpoint(payload: dict):
    user_id = "dev-user"
    trip_id = "4147490b-4117-4a79-b77f-6e9d7da9b8d5"

    request = CreateSessionRequest(
    casino=payload["casino"],
    started_at=datetime.fromisoformat(payload["startedAt"]),
    ended_at=None,
    notes=payload.get("notes", ""),
)

    return create_session_service(request, user_id, trip_id)