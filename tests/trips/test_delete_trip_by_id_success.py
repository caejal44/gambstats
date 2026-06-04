from src.trips.handler import lambda_handler
import json

from tests.helpers.setup_helpers import create_test_trip


def test_delete_trip_by_id_success():
    # create dummy trip
    trip_id = create_test_trip()

    event = {
        "httpMethod": "DELETE",
        "pathParameters": {
            "trip_id": trip_id}
    }

    response = lambda_handler(event, {})

    print("Response:", json.dumps(response, indent=2))

    assert response["statusCode"] == 200

    body = json.loads(response["body"])

    assert body["trip_id"] == trip_id
    assert body["status"] == "deleted"

if __name__ == "__main__":
    test_delete_trip_by_id_success()