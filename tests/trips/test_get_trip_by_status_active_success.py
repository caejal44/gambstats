from src.trips.handler import lambda_handler
import json

from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.setup_helpers import create_test_trip


def test_get_trip_by_status_active_success():
    # create dummy active trip
    trip_id = create_test_trip()

    event = {
        "httpMethod": "GET",
        "queryStringParameters": {
            "status": "active"
        }
    }
    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 200

        body = json.loads(response["body"])

        for trip in body["trips"]:
            assert trip["status"] == "active"

        assert any(trip["trip_id"] == trip_id for trip in body["trips"])

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)

if __name__ == "__main__":
    test_get_trip_by_status_active_success()