import json

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip, cleanup_game
from tests.helpers.setup_helpers import create_test_trip, create_test_session, create_test_game


def test_complete_session_with_active_games():

    # create dummy trip, session, and game
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)
    game_id = create_test_game(session_id)


    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "session_id": session_id},
        "body": json.dumps({
            "ended_at": "2026-05-13T08:00:00Z"
        })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "bad_request"
        assert body["details"] == "cannot complete a session with active games"

    finally:
        # delete dummy trip, session, and games
        cleanup_game(game_id)
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_complete_session_with_active_games()