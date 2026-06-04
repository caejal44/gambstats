import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_game, cleanup_session, cleanup_trip
from tests.helpers.game_helpers import build_game_body
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_create_game_complete_success():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)

    game_id = None

    # Game creation requires an active parent session.
    event = {
        "httpMethod": "POST",
        "pathParameters": {
            "session_id": session_id},
        "body": json.dumps(build_game_body(
            cash_in=0,
            cash_out=245.00,
            ended_at="2026-05-13T05:20:00Z",
            freeplay_used=100.00)
        )
    }

    try:
        response = lambda_handler(event, None)

        assert response["statusCode"] == 201

        body = json.loads(response["body"])

        game_id = body["game_id"]

        assert body["game_name"] == "Glacier Gold"
        assert body["cash_in"] == 0
        assert body["status"] == "completed"

        print("Response:", response)

    finally:
        # delete test game
        if game_id:
            cleanup_game(game_id)

        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_create_game_complete_success()