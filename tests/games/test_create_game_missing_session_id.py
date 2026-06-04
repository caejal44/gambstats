import json

from src.games.handler import lambda_handler


def test_create_game_missing_session_id():

    # Game creation requires an active parent session.
    event = {
        "httpMethod": "POST",
        "body": json.dumps({
            "game_name": "Glacier Gold",
            "game_type": "slot",
            "cash_in": 100.00,
            "started_at": "2026-05-13T05:02:00Z",
            "notes": "Dime denom - 2.00 spins"
        })
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["error"] == "bad_request"
    assert body["details"] == "session_id is required"

    print("Response:", response)


if __name__ == "__main__":
    test_create_game_missing_session_id()