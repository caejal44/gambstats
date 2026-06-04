import json

from src.trips.handler import lambda_handler


def test_update_trip_missing_trip_id():
    event = {
        "httpMethod": "PATCH",
        "body": json.dumps({
            "trip_budget": 1500
        })
    }

    response = lambda_handler(event, {})

    print("Response:", json.dumps(response, indent=2))

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["error"] == "bad_request"
    assert body["details"] == "trip_id is required"


if __name__ == "__main__":
    test_update_trip_missing_trip_id()