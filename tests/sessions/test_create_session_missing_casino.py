import json

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.setup_helpers import create_test_trip


def test_create_session_missing_casino():
    # create dummy completed trip
    trip_id = create_test_trip()

    # Session creation requires an active parent trip.
    event = {
        "httpMethod": "POST",
        "pathParameters": {
            "trip_id": trip_id},
        "body": json.dumps({
            "started_at": "2026-05-12T05:00:00Z",
            "notes": "Morning Slot Session"
        })
    }

    try:
        response = lambda_handler(event, None)

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "validation_error"
        assert body["details"][0]["loc"] == ["casino"]

        print("Response:", response)

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_create_session_missing_casino()