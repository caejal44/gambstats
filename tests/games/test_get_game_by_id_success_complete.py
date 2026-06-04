import json

from src.games.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_game, cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session, \
    create_completed_test_game


def test_get_game_by_id_success_completed():
    # create dummy trip, session, and game
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)
    game_id = create_completed_test_game(session_id)

    event = {
        "httpMethod": "GET",
        "pathParameters": {
            "game_id": game_id}
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["game_id"] == game_id
        assert body["status"] == "completed"
        assert body["cash_out"] is not None

    finally:
        # delete dummy trip, session, and game
        cleanup_game(game_id)
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_get_game_by_id_success_completed()