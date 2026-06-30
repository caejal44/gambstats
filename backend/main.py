from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.trips.service import create_trip as create_trip_service
from src.sessions.service import create_session as create_session_service
from src.sessions.service import show_sessions_by_trip
from src.sessions.service import show_session_by_id
from src.sessions.service import modify_session
from src.games.service import create_game as create_game_service
from src.trips.service import show_all_trips_by_user
from src.trips.service import show_trip_by_id
from src.trips.service import modify_trip
from src.games.service import show_games_by_session
from src.games.service import show_game_by_id
from src.games.service import modify_game

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

class EditGameRequest(BaseModel):
    game_name: Optional[str] 
    game_type: Optional[str]
    cash_in: Optional[float]
    cash_out: Optional[float] 
    started_at: Optional[datetime]
    ended_at: Optional[datetime] 
    entry_mode: str = ""
    notes: Optional[str]
    freeplay_used: Optional[float] 

class EditSessionRequest(BaseModel):
    casino: Optional[str] 
    started_at: Optional[datetime]
    ended_at: Optional[datetime] 
    notes: Optional[str]

class EditTripRequest(BaseModel):
    trip_name: Optional[str] 
    location: Optional[str]
    trip_budget: Optional[float]
    started_at: Optional[datetime]
    ended_at: Optional[datetime] 
    notes: Optional[str]


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

@app.get("/trips")
def get_trips_endpoint(status: Optional[str] = None):
    user_id = "dev-user"
    return show_all_trips_by_user(user_id, status)

@app.get("/sessions")
def get_sessions_endpoint():
    trip_id = "4147490b-4117-4a79-b77f-6e9d7da9b8d5"
    user_id = "dev-user"
    return show_sessions_by_trip(trip_id, user_id)

@app.get("/games")
def get_games_endpoint():
    session_id = "36c0ab8a-004c-47bc-b662-e0041ad62282"
    user_id = "dev-user"
    return show_games_by_session(session_id, user_id)

@app.get("/games/{game_id}")
def get_game_endpoint(game_id: str):
    user_id = "dev-user"
    return show_game_by_id(game_id, user_id)

@app.patch("/games/{game_id}")
def edit_game_endpoint(game_id: str, payload: dict):
    user_id = "dev-user"
    game_id = game_id
    request = EditGameRequest(
    game_name=payload["gameName"],
    game_type=payload["gameType"],
    cash_in=payload["cashIn"],
    cash_out=payload["cashOut"],
    started_at=(datetime.fromisoformat(payload["startedAt"])
    if payload.get("startedAt") else None),
    ended_at=(datetime.fromisoformat(payload["endedAt"])
    if payload.get("endedAt") else None),
    notes=payload.get("notes", ""),
    entry_mode="",
    freeplay_used= payload.get("freeplayUsed"),
)

    return modify_game(request, game_id, user_id,)

@app.get("/sessions/{session_id}")
def get_session_endpoint(session_id: str):
    user_id = "dev-user"
    return show_session_by_id(session_id, user_id)

@app.patch("/sessions/{session_id}")
def edit_session_endpoint(session_id: str, payload: dict):
    user_id = "dev-user"
    session_id = session_id
    request = EditSessionRequest(
    casino=payload["casino"],
    started_at=(datetime.fromisoformat(payload["startedAt"])
    if payload.get("startedAt") else None),
    ended_at=(datetime.fromisoformat(payload["endedAt"])
    if payload.get("endedAt") else None),
    notes=payload.get("notes", ""),
)

    return modify_session(request, session_id, user_id,)

@app.get("/trips/{trip_id}")
def get_trip_endpoint(trip_id: str):
    return show_trip_by_id(trip_id)

@app.patch("/trips/{trip_id}")
def edit_trip_endpoint(trip_id: str, payload: dict):
    user_id = "dev-user"
    trip_id = trip_id
    request = EditTripRequest(
    trip_name=payload["tripName"],
    location=payload["location"],
    trip_budget=payload["tripBudget"],
    started_at=(datetime.fromisoformat(payload["startedAt"])
    if payload.get("startedAt") else None),
    ended_at=(datetime.fromisoformat(payload["endedAt"])
    if payload.get("endedAt") else None),
    notes=payload.get("notes", ""),
)

    return modify_trip(request, trip_id, user_id,)