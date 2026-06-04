from src.games.repository import delete_game
from src.sessions.repository import delete_session
from src.trips.repository import delete_trip


def cleanup_game(game_id) -> None:
    delete_game(game_id)

def cleanup_session(session_id) -> None:
    delete_session(session_id)

def cleanup_trip(trip_id) -> None:
    delete_trip(trip_id)