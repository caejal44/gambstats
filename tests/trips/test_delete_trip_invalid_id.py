from src.trips.handler import lambda_handler
import json

from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.setup_helpers import create_test_trip


def test_delete_trip_invalid_id():
    # create dummy trip
    trip_id = create_test_trip()
    invalid_trip_id = trip_id[:-1] + "x"

    event = {
        "httpMethod": "DELETE",
        "pathParameters": {
            "trip_id": invalid_trip_id}
    }

    try:
        response = lambda_handler(event, {})

        print("Response:", json.dumps(response, indent=2))

        assert response["statusCode"] == 404

        body = json.loads(response["body"])

        assert body["error"] == "not_found"
        assert body["details"] == "trip not found"

    finally:
        # delete dummy trip
        cleanup_trip(trip_id)

if __name__ == "__main__":
    test_delete_trip_invalid_id()