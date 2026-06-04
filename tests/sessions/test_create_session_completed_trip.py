import json

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.session_helpers import build_session_body
from tests.helpers.setup_helpers import create_completed_test_trip


def test_create_session_completed_trip():
    # create dummy completed trip
    trip_id = create_completed_test_trip()

    # Session creation requires an active parent trip.
    event = {
        "httpMethod": "POST",
        "pathParameters": {
            "trip_id": trip_id},
        "body": json.dumps(build_session_body()
        )
    }

    try:
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "bad_request"
        assert body["details"] == "trip must be active to create a session"

        print("Response:", response)

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_create_session_completed_trip()