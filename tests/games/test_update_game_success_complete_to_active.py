import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_game, cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session, create_completed_test_game


def test_update_game_success_complete_to_active():
    # create dummy trip, session, and game
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)
    game_id = create_completed_test_game(session_id)

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "game_id": game_id},
        "body": json.dumps({
            "game_name": "Glacier Gold - Ultimate Fire Link",
            "cash_in": 250.00,
            "cash_out": None,
            "ended_at": None,
            "notes": "Dime Denom - 2.00 bets - 100 rebuy"
    })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["game_name"] == "Glacier Gold - Ultimate Fire Link"
        assert body["cash_in"] == 250.00
        assert body["notes"] == "Dime Denom - 2.00 bets - 100 rebuy"
        assert body["status"] == "active"

    finally:
        # delete dummy trip, session, and game
        cleanup_game(game_id)
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_game_success_complete_to_active()