import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_create_game_missing_cash_in():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)

    # Game creation requires an active parent session.
    event = {
        "httpMethod": "POST",
        "pathParameters": {
            "session_id": session_id},
        "body": json.dumps({
            "game_name": "China Street",
            "game_type": "slot",
            "started_at": "2026-05-13T05:15:00Z",
            "notes": "Dime denom - 2.00 spins"
        })
    }

    try:
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "validation_error"
        assert body["details"][0]["loc"][-1] == "cash_in"

        print("Response:", response)

    finally:
        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)

if __name__ == "__main__":
    test_create_game_missing_cash_in()