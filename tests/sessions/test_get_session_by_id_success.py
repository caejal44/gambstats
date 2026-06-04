from src.sessions.handler import lambda_handler
import json

from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_get_session_by_id_success():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)

    event = {
        "httpMethod": "GET",
        "pathParameters": {
            "session_id": session_id}
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["session_id"] == session_id
        assert body["status"] == "active"

    finally:
        # delete dummy trip and session
        cleanup_session(session_id)
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_get_session_by_id_success()