import json

from src.sessions.handler import lambda_handler


def test_delete_session_missing_session_id():
    event = {
        "httpMethod": "DELETE"
    }

    response = lambda_handler(event, {})

    print("Response:", json.dumps(response, indent=2))

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["error"] == "bad_request"
    assert body["details"] == "session_id is required"


if __name__ == "__main__":
    test_delete_session_missing_session_id()