import json

from src.games.handler import lambda_handler


def test_update_game_missing_game_id():
    event = {
        "httpMethod": "PATCH",
        "body": json.dumps({
            "cash_in": 25,
            "cash_out": 25.34,
            "started_at": "2026-05-13T05:18:00Z",
            "ended_at": "2026-05-13T05:36:00Z",
            "notes": "Dime denom"
    })
    }

    response = lambda_handler(event, {})

    print("Response:", json.dumps(response, indent=2))

    assert response["statusCode"] == 400

    body = json.loads(response["body"])

    assert body["error"] == "bad_request"
    assert body["details"] == "game_id is required"


if __name__ == "__main__":
    test_update_game_missing_game_id()