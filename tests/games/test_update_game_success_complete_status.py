import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_game, cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session, create_test_game


def test_update_game_success_complete_status():
    # create dummy trip, session, and game
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)
    game_id = create_test_game(session_id)

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "game_id": game_id},
        "body": json.dumps({
            "cash_in": 150.00,
            "cash_out": 0,
            "ended_at": "2026-05-13T05:18:00Z",
            "notes": "Dime denom - 2.00 spins - 50 rebuy in"
    })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["cash_in"] == 150.00
        assert body["ended_at"] == "2026-05-13T05:18:00+00:00"
        assert body["cash_out"] == 0
        assert body["notes"] == "Dime denom - 2.00 spins - 50 rebuy in"
        assert body["status"] == "completed"

    finally:
        # delete dummy trip, session, and game
        cleanup_game(game_id)
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_game_success_complete_status()