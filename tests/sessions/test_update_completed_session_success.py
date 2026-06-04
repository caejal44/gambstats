import json

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_completed_test_session, create_test_trip


def test_update_completed_session_success():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_completed_test_session(trip_id)

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "session_id": session_id},
        "body": json.dumps({
            "ended_at": "2026-05-13T12:00:00Z",
            "notes": "Morning Craps Session"
    })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["notes"] == "Morning Craps Session"

    finally:
        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_completed_session_success()