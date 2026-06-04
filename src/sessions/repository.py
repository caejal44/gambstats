from typing import Optional, List

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sessions')

def save_session(session: dict) -> None:
    table.put_item(Item=session)

def get_session(session_id: str) -> Optional[dict]:
    response = table.get_item(Key={"session_id": session_id})
    return response.get('Item')

def get_sessions_by_trip(trip_id: str) -> List[dict]:
    response = table.query(IndexName="trip_id-created_at-index", KeyConditionExpression=Key("trip_id").eq(trip_id))
    return response.get("Items", [])

def update_session(session: dict) -> None:
    table.put_item(Item=session)

def delete_session(session_id: str) -> None:
    table.delete_item(Key={"session_id": session_id})