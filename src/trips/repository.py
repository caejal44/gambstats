from typing import List, Optional

import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('trips')

def save_trip(trip: dict) -> None:
    table.put_item(Item=trip)

def get_trip(trip_id: str) -> Optional[dict]:
    response = table.get_item(Key={"trip_id": trip_id})
    return response.get("Item")

def get_trips_by_user(user_id: str) -> List[dict]:
    response = table.query(IndexName="user_id-created_at-index", KeyConditionExpression=Key("user_id").eq(user_id))
    return response.get("Items", [])

def update_trip(trip: dict) -> None:
    table.put_item(Item=trip)

def delete_trip(trip_id: str) -> None:
    table.delete_item(Key={"trip_id": trip_id})
    
