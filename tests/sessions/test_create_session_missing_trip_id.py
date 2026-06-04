import json

from src.sessions.handler import lambda_handler


def test_create_session_missing_trip_id():
    # Session creation requires an active parent trip.
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "casino": "Hard Rock",
            "started_at": "2026-05-12T05:00:00Z",
            "notes": "Morning Slot Session"
        })
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["error"] == "bad_request"
    assert body["details"] == "trip_id is required"

    print("Response:", response)


if __name__ == "__main__":
    test_create_session_missing_trip_id()