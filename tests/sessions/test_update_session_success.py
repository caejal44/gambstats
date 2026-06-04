import json

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_update_session_success():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "session_id": session_id},
        "body": json.dumps({
            "started_at": "2026-05-12T11:00:00Z",
            "ended_at": "2026-05-12T12:00:00Z",
            "notes": "Morning Craps Session"
    })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["started_at"] == "2026-05-12T11:00:00+00:00"
        assert body["ended_at"] == "2026-05-12T12:00:00+00:00"
        assert body["notes"] == "Morning Craps Session"

    finally:
        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_session_success()