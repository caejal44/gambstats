import json

from src.trips.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.setup_helpers import create_completed_test_trip


def test_update_trip_invalid_ended_at():
    # create completed dummy trip
    trip_id = create_completed_test_trip()

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "trip_id": trip_id},
        "body": json.dumps({
            "ended_at": "2026-02-01T08:00:00Z"
        })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "bad_request"
        assert body["details"] == "trip started_at must be before trip ended_at"

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_trip_invalid_ended_at()