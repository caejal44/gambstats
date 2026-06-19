from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.trips.service import create_trip as create_trip_service

app = FastAPI()

class CreateTripRequest(BaseModel):
    trip_name: str
    location: str
    trip_budget: str
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