from typing import Optional, List

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('games')

def save_game(game: dict) -> None:
    table.put_item(Item=game)

def get_game(game_id: str) -> Optional[dict]:
    response = table.get_item(Key={"game_id": game_id})
    return response.get('Item')

def get_games_by_session(session_id: str) -> List[dict]:
    response = table.query(IndexName="session_id-created_at-index", KeyConditionExpression=Key("session_id").eq(session_id))
    return response.get("Items", [])

def update_game(game: dict) -> None:
    table.put_item(Item=game)

def delete_game(game_id: str) -> None:
    table.delete_item(Key={"game_id": game_id})
