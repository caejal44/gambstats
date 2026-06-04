import json

from src.trips.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_delete_trip_with_sessions():

    # create dummy trip, session, and game
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)


    event = {
        "httpMethod": "DELETE",
        "pathParameters": {
            "trip_id": trip_id}
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "bad_request"
        assert body["details"] == "cannot delete a trip with sessions"

    finally:
        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_delete_trip_with_sessions()