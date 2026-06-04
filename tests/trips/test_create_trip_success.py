from src.trips.handler import lambda_handler
import json

from tests.helpers.cleanup_helpers import cleanup_trip
from tests.helpers.trip_helpers import build_trip_body


def test_create_trip_success():

    trip_id = None

    event = {
        "httpMethod": "POST",
        "body": json.dumps(
            build_trip_body()
        )
    }

    try:
        response = lambda_handler(event, None)

        print("Response:", response)

        assert response["statusCode"] == 201

        body = json.loads(response["body"])

        trip_id = body["trip_id"]

        assert body["location"] == "Las Vegas"
        assert body["status"] == "active"

    finally:
        cleanup_trip(trip_id)


if __name__ == "__main__":
    test_create_trip_success()