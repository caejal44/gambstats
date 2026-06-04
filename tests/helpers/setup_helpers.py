import json

from tests.helpers.game_helpers import build_game_body
from tests.helpers.session_helpers import build_session_body
from tests.helpers.trip_helpers import build_trip_body
from src.trips.handler import lambda_handler as trip_handler
from src.sessions.handler import lambda_handler as session_handler
from src.games.handler import lambda_handler as game_handler


def create_test_trip():
    event = {
        "httpMethod": "POST",
        "body": json.dumps(build_trip_body())
    }

    response = trip_handler(event, {})

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["location"] == "Las Vegas"
    assert body["status"] == "active"

    return body["trip_id"]

def create_completed_test_trip(ended_at="2026-05-16T05:00:00Z"):
    event = {
        "httpMethod": "POST",
        "body": json.dumps(build_trip_body(ended_at=ended_at))
    }

    response = trip_handler(event, {})

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["location"] == "Las Vegas"
    assert body["status"] == "completed"

    return body["trip_id"]

def create_test_session(trip_id):
    event = {
        "httpMethod": "POST",
        "pathParameters": {"trip_id": trip_id},
        "body": json.dumps(build_session_body())
    }

    response = session_handler(event, {})

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["casino"] == "Aria"
    assert body["status"] == "active"

    return body["session_id"]

def create_completed_test_session(trip_id, ended_at="2026-05-13T05:30:00Z"):
    event = {
        "httpMethod": "POST",
        "pathParameters": {"trip_id": trip_id},
        "body": json.dumps(build_session_body(ended_at=ended_at))
    }

    response = session_handler(event, {})

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["casino"] == "Aria"
    assert body["status"] == "completed"

    return body["session_id"]

def create_test_game(session_id):
    event = {
        "httpMethod": "POST",
        "pathParameters": {"session_id": session_id},
        "body": json.dumps(build_game_body())
    }

    response = game_handler(event, {})

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["game_name"] == "Glacier Gold"
    assert body["status"] == "active"

    return body["game_id"]

def create_completed_test_game(session_id,
                               cash_out=125.00,
                               ended_at="2026-05-13T05:12:00Z"):
    event = {
        "httpMethod": "POST",
        "pathParameters": {"session_id": session_id},
        "body": json.dumps(build_game_body(cash_out=cash_out,
                                           ended_at=ended_at))
    }

    response = game_handler(event, {})

    assert response["statusCode"] == 201

    body = json.loads(response["body"])

    assert body["cash_out"] == 125.00
    assert body["status"] == "completed"

    return body["game_id"]