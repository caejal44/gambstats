from datetime import datetime
from decimal import Decimal

from src.common.exceptions import BadRequestError, NotFoundError
from src.common.utils import create_id, get_timestamp
from src.games.repository import save_game, get_game, get_games_by_session, update_game, delete_game
from src.games.schemas import GameResponse, CreateGameRequest, GameListResponse, UpdateGameRequest
from src.sessions.service import show_session_by_id


def create_game(request: CreateGameRequest, user_id: str, session_id: str) -> GameResponse:
    """
    Creates a game under an existing user-owned session.
    Games with cash_out are created as completed; games without cash_out are active.
    """

    parent_session = show_session_by_id(session_id, user_id)

    if parent_session.status != "active":
        raise BadRequestError("session must be active to create a game")

    game = {
        "game_id": create_id(),
        "session_id": session_id,
        "trip_id": parent_session.trip_id,
        "user_id": user_id,
        "game_name": request.game_name,
        "game_type": request.game_type,
        "cash_in": Decimal(str(request.cash_in)),
        "cash_out": Decimal(str(request.cash_out)) if request.cash_out is not None else None,
        "status": "completed" if request.cash_out is not None else "active",
        "started_at": request.started_at.isoformat() if request.started_at else None,
        "ended_at": request.ended_at.isoformat() if request.ended_at else None,
        "created_at": get_timestamp(),
        "notes": request.notes,
        "entry_mode": request.entry_mode,
        "freeplay_used": Decimal(str(request.freeplay_used)) if request.freeplay_used is not None else None
    }

    save_game(game)

    return GameResponse(**game)

def show_game_by_id(game_id: str, user_id: str ) -> GameResponse:
    game = get_game(game_id)
    if game is None:
        raise NotFoundError("game not found")
    if user_id != game["user_id"]:
        raise BadRequestError("user_id not allowed to access this game")
    return GameResponse(**game)

def show_games_by_session(session_id: str, user_id: str) -> GameListResponse:
    # Validates that the parent session exists and belongs to the user.
    show_session_by_id(session_id, user_id)

    games = get_games_by_session(session_id)
    return GameListResponse(
        games=[GameResponse(**game) for game in games]
    )

def modify_game(request: UpdateGameRequest, game_id: str, user_id: str) -> GameResponse:
    # User cannot modify user_id, trip_id, session_id, game_id or status.
    # Status updates to completed when cash_out is provided.
    # Status reverts to active if cash_out is removed.
    game = get_game(game_id)

    if game is None:
        raise NotFoundError("game not found")

    if user_id != game["user_id"]:
        raise BadRequestError("user_id not allowed to modify this game")

    updates = request.model_dump(exclude_unset=True)

    if "started_at" in updates and updates["started_at"] is not None:
        updates["started_at"] = updates["started_at"].isoformat()

    if "ended_at" in updates and updates["ended_at"] is not None:
        updates["ended_at"] = updates["ended_at"].isoformat()

    if "cash_in" in updates and updates["cash_in"] is not None:
        updates["cash_in"] = Decimal(str(updates["cash_in"]))

    if "cash_out" in updates and updates["cash_out"] is not None:
        updates["cash_out"] = Decimal(str(updates["cash_out"]))

    if "freeplay_used" in updates and updates["freeplay_used"] is not None:
        updates["freeplay_used"] = Decimal(str(updates["freeplay_used"]))

    updated_game = {**game, **updates}

    # A game with ended_at must have cash_out, and cannot end before it starts.
    if updated_game["ended_at"] is not None:
        if updated_game["started_at"] is not None:
            # convert to datetime for comparison
            ended_at = datetime.fromisoformat(updated_game["ended_at"])
            started_at = datetime.fromisoformat(updated_game["started_at"])
            if ended_at <= started_at:
                raise BadRequestError("game started_at must be before game ended_at")
        if updated_game["cash_out"] is None:
            raise BadRequestError("if ended_at exists, cash_out must exist")

    # freeplay_used must be > 0 if cash_in is 0
    if updated_game["cash_in"] == 0:
        if updated_game["freeplay_used"] is None or updated_game["freeplay_used"] <= 0:
            raise BadRequestError("freeplay_used must be greater than 0 if cash_in equals 0")

    # status must be completed if cash_out is entered
    if updated_game["cash_out"] is not None:
        updated_game["status"] = "completed"
    else:
        updated_game["status"] = "active"

    update_game(updated_game)

    return GameResponse(**updated_game)

def delete_game_by_id(game_id: str, user_id: str) -> dict:
    game = get_game(game_id)
    if game is None:
        raise NotFoundError("game not found")
    if user_id != game["user_id"]:
        raise BadRequestError("user_id not allowed to delete this game")
    delete_game(game_id)
    return {
        "game_id": game_id,
        "status": "deleted"
    }

