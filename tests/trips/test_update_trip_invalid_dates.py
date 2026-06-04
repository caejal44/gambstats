import json

from src.trips.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.setup_helpers import create_test_trip


def test_update_trip_invalid_dates():
    # create dummy trip
    trip_id = create_test_trip()

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "trip_id": trip_id,},
        "body": json.dumps({
            "started_at": "2026-06-10T08:00:00Z",
            "ended_at": "2026-06-09T08:00:00Z",
        })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 400

        body = json.loads(response["body"])

        assert body["error"] == "validation_error"
        assert "ended_at cannot be before started_at" in str(body["details"])

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_trip_invalid_dates()