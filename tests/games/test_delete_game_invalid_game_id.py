import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_game, cleanup_trip
from tests.helpers.setup_helpers import create_test_game, create_test_trip, create_test_session


def test_delete_game_invalid_game_id():
    # create dummy trip, session, and game
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)
    game_id = create_test_game(session_id)

    invalid_game_id = game_id[:-1] + "x"

    event = {
        "httpMethod": "DELETE",
        "pathParameters": {
            "game_id": invalid_game_id}
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 404

        body = json.loads(response["body"])

        assert body["error"] == "not_found"
        assert body["details"] == "game not found"

    finally:
        # delete dummy trip, session, and game
        cleanup_game(game_id)
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_delete_game_invalid_game_id()