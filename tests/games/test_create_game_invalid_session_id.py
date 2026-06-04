import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.game_helpers import build_game_body
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_create_game_invalid_session_id():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)

    invalid_session_id = session_id[:-1] + "x"

    # Game creation requires an active parent session.
    event = {
        "httpMethod": "POST",
        "pathParameters": {
            "session_id": invalid_session_id},
        "body": json.dumps(build_game_body()
        )
    }

    try:
        response = lambda_handler(event, None)

        assert response["statusCode"] == 404

        body = json.loads(response["body"])

        assert body["error"] == "not_found"
        assert body["details"] == "session not found"

        print("Response:", response)

    finally:
        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)

if __name__ == "__main__":
    test_create_game_invalid_session_id()