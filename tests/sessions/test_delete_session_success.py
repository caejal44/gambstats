import json

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session


def test_delete_session_success():
    # create dummy trip and session
    trip_id = create_test_trip()
    session_id = create_test_session(trip_id)

    event = {
        "httpMethod": "DELETE",
        "pathParameters": {
            "session_id": session_id}
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["session_id"] == session_id
        assert body["status"] == "deleted"

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_delete_session_success()