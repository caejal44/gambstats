import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.game_helpers import build_game_body
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_create_game_invalid_freeplay_used():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)

    # Game creation requires an active parent session.
    event = {
        "httpMethod": "POST",
        "pathParameters": {
            "session_id": session_id},
        "body": json.dumps(build_game_body(
            cash_in=0,
            cash_out=150,
            started_at="2026-05-13T05:15:00Z",
            ended_at="2026-05-13T05:20:00Z",
            freeplay_used=0)
        )
    }

    try:
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "validation_error"
        assert "freeplay_used must be greater than 0 if cash_in is 0" in str(body["details"])

        print("Response:", response)

    finally:
        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)

if __name__ == "__main__":
    test_create_game_invalid_freeplay_used()