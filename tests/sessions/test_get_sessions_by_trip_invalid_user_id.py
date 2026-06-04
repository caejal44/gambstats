import json
import pytest

from src.sessions.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_session, cleanup_trip
from tests.helpers.setup_helpers import create_test_trip, create_test_session

@pytest.mark.skip(reason="Requires authentication implementation")
def test_get_sessions_by_trip_invalid_user_id():
    # create dummy trip
    trip_id = create_test_trip()

    event = {
        "httpMethod": "GET",
        "pathParameters": {
            "user_id": "user231",
            "trip_id": trip_id}
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "bad_request"
        assert body["details"] == "user_id not allowed to access sessions for this trip"

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_get_sessions_by_trip_invalid_user_id()