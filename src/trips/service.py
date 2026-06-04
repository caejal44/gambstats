from datetime import datetime
from typing import Optional

from src.common.exceptions import NotFoundError, BadRequestError
from src.common.utils import create_id, get_timestamp
from src.sessions.repository import get_sessions_by_trip
from src.trips.repository import save_trip, get_trip, get_trips_by_user, delete_trip, update_trip
from src.trips.schemas import CreateTripRequest, TripResponse, TripListResponse, UpdateTripRequest
from decimal import Decimal


def create_trip(request: CreateTripRequest, user_id: str) -> TripResponse:
    # MVP lifecycle: trips are active by default. Planned trips may be added later.
    # Providing ended_at creates or updates the trip as completed.
    trip = {
        "trip_id": create_id(),
        "user_id": user_id,
        "trip_name": request.trip_name,
        "location": request.location,
        "trip_budget": Decimal(str(request.trip_budget)),
        "started_at": request.started_at.isoformat(),
        "ended_at": request.ended_at.isoformat() if request.ended_at else None,
        "status": "completed" if request.ended_at is not None else "active",
        "created_at": get_timestamp(),
        "notes": request.notes
    }
    save_trip(trip)
    return TripResponse(**trip)

def show_trip_by_id(trip_id: str) -> TripResponse:
    trip = get_trip(trip_id)
    if trip is None:
        raise NotFoundError("trip not found")
    return TripResponse(**trip)

def show_all_trips_by_user(user_id: str, status: Optional[str]) -> TripListResponse:
    trips = get_trips_by_user(user_id)
    allowed_statuses = ["active", "completed"]
    if status is not None:
        if status not in allowed_statuses:
            raise BadRequestError("status not allowed")

        trips=[trip for trip in trips if trip["status"] == status]

    return TripListResponse(
        trips=[TripResponse(**trip) for trip in trips])

def modify_trip(request: UpdateTripRequest, trip_id: str, user_id: str) -> TripResponse:
    # User cannot modify user_id, trip_id, created_at or status.
    # Status updates to completed when ended_at is provided
    # and all child sessions are completed.
    trip = get_trip(trip_id)

    if trip is None:
        raise NotFoundError("trip not found")

    if user_id != trip["user_id"]:
        raise BadRequestError("user_id not allowed to modify this trip")

    # if trip["status"] == "completed":
        raise BadRequestError("trip cannot be changed if completed")

    updates = request.model_dump(exclude_unset=True)

    if "started_at" in updates and updates["started_at"] is not None:
        updates["started_at"] = updates["started_at"].isoformat()

    if "ended_at" in updates and updates["ended_at"] is not None:
        updates["ended_at"] = updates["ended_at"].isoformat()

    if "trip_budget" in updates and updates["trip_budget"] is not None:
        updates["trip_budget"] = Decimal(str(updates["trip_budget"]))

    updated_trip = {**trip, **updates}

    if updated_trip["ended_at"] is not None:
        # convert to datetime for comparison
        ended_at = datetime.fromisoformat(updated_trip["ended_at"])
        started_at = datetime.fromisoformat(updated_trip["started_at"])
        if ended_at <= started_at:
            raise BadRequestError("trip started_at must be before trip ended_at")

        sessions = get_sessions_by_trip(trip_id)

        has_open_sessions = any(
            session["status"] != "completed"
            for session in sessions
        )

        if has_open_sessions:
            raise BadRequestError("cannot complete a trip with active sessions")

        updated_trip["status"] = "completed"

    update_trip(updated_trip)

    return TripResponse(**updated_trip)

def delete_trip_by_id(trip_id: str, user_id: str) -> dict:
    # User cannot delete a trip with child sessions
    trip = get_trip(trip_id)

    if trip is None:
        raise NotFoundError("trip not found")

    if user_id != trip["user_id"]:
        raise BadRequestError("user_id not allowed to delete this trip")

    sessions = get_sessions_by_trip(trip_id)
    if sessions:
        raise BadRequestError("cannot delete a trip with sessions")

    delete_trip(trip["trip_id"])

    return {
        "trip_id": trip["trip_id"],
        "status": "deleted"
    }
