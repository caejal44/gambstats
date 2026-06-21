from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.trips.service import create_trip as create_trip_service
from src.sessions.service import create_session as create_session_service
from src.games.service import create_game as create_game_service

app = FastAPI()


class CreateTripRequest(BaseModel):
    trip_name: str
    location: str
    trip_budget: float
    started_at: datetime
    ended_at: Optional[datetime] = None
    notes: str = ""

class CreateSessionRequest(BaseModel):
    casino: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    notes: str = ""

class CreateGameRequest(BaseModel):
    game_name: str
    game_type: str
    cash_in: float
    cash_out: Optional[float] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    entry_mode: str = ""
    notes: str = ""
    freeplay_used: Optional[float] = None

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

@app.post("/games")
def create_game_endpoint(payload: dict):
    user_id = "dev-user"
    session_id = "36c0ab8a-004c-47bc-b662-e0041ad62282"

    request = CreateGameRequest(
    game_name=payload["gameName"],
    game_type=payload["gameType"],
    cash_in=payload["cashIn"],
    cash_out=None,
    started_at=(datetime.fromisoformat(payload["startedAt"])
    if payload.get("startedAt") else None),
    ended_at=None,
    notes=payload.get("notes", ""),
    entry_mode="",
    freeplay_used= payload.get("freeplayUsed"),
)

    return create_game_service(request, user_id, session_id)