import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_game, cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session, create_test_game


def test_update_game_active_success():
    # create dummy trip, session, and game
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)
    game_id = create_test_game(session_id)

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "game_id": game_id},
        "body": json.dumps({
            "cash_in": 225,
            "started_at": "2026-05-13T05:05:00Z",
            "notes": "Nickel Denom - 1.00 bets"
    })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["started_at"] == "2026-05-13T05:05:00+00:00"
        assert body["cash_in"] == 225
        assert body["notes"] == "Nickel Denom - 1.00 bets"

    finally:
        # delete dummy trip, session, and game
        cleanup_game(game_id)
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_game_active_success()