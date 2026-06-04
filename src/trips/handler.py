import json

from src.common.responses import success_response, error_response
from src.common.utils import get_current_user_id, error_handler, get_required_path_param
from src.trips.schemas import CreateTripRequest, UpdateTripRequest
from src.trips.service import create_trip, show_trip_by_id, show_all_trips_by_user, modify_trip, delete_trip_by_id

@error_handler
def lambda_handler(event, context):
    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")

    user_id = get_current_user_id(event)

    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        request = CreateTripRequest(**body)
        trip = create_trip(request, user_id)
        return success_response(201, trip.model_dump())


    elif method == "GET":
        # GET supports both list and detail views:
        # /trips and /trips/{trip_id}

        path_params = event.get("pathParameters") or {}
        trip_id = path_params.get("trip_id")
        query_params = event.get("queryStringParameters") or {}
        status = query_params.get("status")

        if trip_id:
            trip = show_trip_by_id(trip_id)
            return success_response(200, trip.model_dump())
        trips = show_all_trips_by_user(user_id, status)
        return success_response(200, trips.model_dump())

    elif method == "PATCH":
        # PATCH and DELETE require a specific trip_id.
        trip_id = get_required_path_param(event, "trip_id")

        body = json.loads(event.get("body") or "{}")
        request = UpdateTripRequest(**body)
        trip = modify_trip(request, trip_id, user_id)
        return success_response(200, trip.model_dump())


    elif method == "DELETE":
        trip_id = get_required_path_param(event, "trip_id")
        result = delete_trip_by_id(trip_id, user_id)
        return success_response(200, result)

    else:
        return error_response(405, "method_not_allowed")










