from src.trips.handler import lambda_handler
import json


def test_get_trip_by_invalid_status():

    event = {
        "httpMethod": "GET",
        "queryStringParameters": {
            "status": "rock"
        }
    }

    response = lambda_handler(event, {})

    print("Response:", json.dumps(response, indent=2))

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["error"] == "bad_request"
    assert body["details"] == "status not allowed"

if __name__ == "__main__":
    test_get_trip_by_invalid_status()