import json

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_trip, cleanup_session
from tests.helpers.session_helpers import build_session_body
from tests.helpers.setup_helpers import create_test_trip


def test_create_session_success():
    # create dummy completed trip
    trip_id = create_test_trip()

    session_id = None

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

        assert response["statusCode"] == 201

        body = json.loads(response["body"])

        session_id = body["session_id"]

        assert body["casino"] == "Aria"
        assert body["status"] == "active"

        print("Response:", response)

    finally:
        if session_id:
            cleanup_session(session_id)

        cleanup_trip(trip_id)

if __name__ == "__main__":
    test_create_session_success()