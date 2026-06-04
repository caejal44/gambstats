from datetime import datetime

from src.common.exceptions import BadRequestError, NotFoundError
from src.common.utils import create_id, get_timestamp
from src.games.repository import get_games_by_session
from src.sessions.repository import save_session, get_session, get_sessions_by_trip, update_session, delete_session
from src.sessions.schemas import SessionResponse, CreateSessionRequest, SessionListResponse, UpdateSessionRequest
from src.trips.service import show_trip_by_id


def create_session(request: CreateSessionRequest, user_id: str, trip_id: str) -> SessionResponse:
    """
    Creates an active session under an existing user-owned trip.
    Sessions can only be created under an active trip.
    """

    parent_trip = show_trip_by_id(trip_id)

    if user_id != parent_trip.user_id:
        raise BadRequestError("user_id not allowed to create this session")

    if parent_trip.status != "active":
        raise BadRequestError("trip must be active to create a session")

    session = {
        "session_id": create_id(),
        "user_id": user_id,
        "trip_id": trip_id,
        "casino": request.casino,
        "started_at": request.started_at.isoformat(),
        "ended_at": request.ended_at.isoformat() if request.ended_at else None,
        "status": "completed" if request.ended_at is not None else "active",
        "created_at": get_timestamp(),
        "notes": request.notes
    }

    save_session(session)

    return SessionResponse(**session)

def show_session_by_id(session_id: str, user_id: str ) -> SessionResponse:
    session = get_session(session_id)
    if session is None:
        raise NotFoundError("session not found")
    if user_id != session["user_id"]:
        raise BadRequestError("user_id not allowed to access this session")
    return SessionResponse(**session)

def show_sessions_by_trip(trip_id: str, user_id: str) -> SessionListResponse:
    parent_trip = show_trip_by_id(trip_id)
    if user_id != parent_trip.user_id:
        raise BadRequestError("user_id not allowed to access sessions for this trip")
    sessions = get_sessions_by_trip(trip_id)
    return SessionListResponse(
        sessions=[SessionResponse(**session) for session in sessions]
    )

def modify_session(request: UpdateSessionRequest, session_id: str, user_id: str) -> SessionResponse:
    # User cannot modify user_id, trip_id, session_id or status.
    # Status updates to completed when ended_at is provided
    # and all child games are completed.
    session = get_session(session_id)

    if session is None:
        raise NotFoundError("session not found")

    if user_id != session["user_id"]:
        raise BadRequestError("user_id not allowed to modify this session")

    # if session["status"] == "completed":
        raise BadRequestError("session cannot be changed if completed")

    updates = request.model_dump(exclude_unset=True)

    if "started_at" in updates and updates["started_at"] is not None:
        updates["started_at"] = updates["started_at"].isoformat()

    if "ended_at" in updates and updates["ended_at"] is not None:
        updates["ended_at"] = updates["ended_at"].isoformat()

    updated_session = {**session, **updates}

    if updated_session["ended_at"] is not None:
        # convert to datetime for comparison
        ended_at = datetime.fromisoformat(updated_session["ended_at"])
        started_at = datetime.fromisoformat(updated_session["started_at"])
        if ended_at <= started_at:
            raise BadRequestError("session started_at must be before session ended_at")

        games = get_games_by_session(session_id)

        has_open_games = any(
            game["status"] != "completed"
            for game in games
        )

        if has_open_games:
            raise BadRequestError("cannot complete a session with active games")

        updated_session["status"] = "completed"

    update_session(updated_session)

    return SessionResponse(**updated_session)

def delete_session_by_id(session_id: str, user_id: str) -> dict:
    # User cannot delete a session with child games.
    session = get_session(session_id)
    if session is None:
        raise NotFoundError("session not found")
    if user_id != session["user_id"]:
        raise BadRequestError("user_id not allowed to delete this session")

    games = get_games_by_session(session_id)
    if games:
        raise BadRequestError("cannot delete a session with games")

    delete_session(session_id)
    return {
        "session_id": session_id,
        "status": "deleted"
    }







