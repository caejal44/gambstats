import json

from src.trips.handler import lambda_handler
from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.setup_helpers import create_test_trip


def test_update_trip_success():
    # create dummy trip
    trip_id = create_test_trip()

    event = {
        "httpMethod": "PATCH",
        "pathParameters": {
            "trip_id": trip_id},
        "body": json.dumps({
            "trip_budget": 1000,
            "started_at": "2026-06-11T08:00:00Z",
            "ended_at": "2026-06-18T08:00:00Z",
            "notes": "Birthday Trip"
        })
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        assert body["trip_budget"] == 1000
        assert body["status"] == "completed"
        assert body["notes"] == "Birthday Trip"

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_update_trip_success()