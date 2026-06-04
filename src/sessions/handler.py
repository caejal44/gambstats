import json

from src.common.responses import success_response, error_response
from src.common.utils import get_required_path_param, get_current_user_id, error_handler
from src.sessions.schemas import CreateSessionRequest, UpdateSessionRequest
from src.sessions.service import create_session, show_session_by_id, show_sessions_by_trip, modify_session, \
    delete_session_by_id

@error_handler
def lambda_handler(event, context):
    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")

    user_id = get_current_user_id(event)

    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        request = CreateSessionRequest(**body)
        trip_id = get_required_path_param(event, "trip_id")
        session = create_session(request, user_id, trip_id)
        return success_response(201, session.model_dump())

    elif method == "GET":
        # GET supports both list and detail views:
        # /sessions and /sessions/{session_id}
        path_params = event.get("pathParameters") or {}
        session_id = path_params.get("session_id")

        if session_id:
            session = show_session_by_id(session_id, user_id)
            return success_response(200, session.model_dump())

        trip_id = get_required_path_param(event, "trip_id")
        sessions = show_sessions_by_trip(trip_id, user_id)
        return success_response(200, sessions.model_dump())

    elif method == "PATCH":
        # PATCH and DELETE require a specific session_id.
        session_id = get_required_path_param(event, "session_id")
        body = json.loads(event.get("body") or "{}")
        request = UpdateSessionRequest(**body)
        session = modify_session(request, session_id, user_id)
        return success_response(200, session.model_dump())

    elif method == "DELETE":

        session_id = get_required_path_param(event, "session_id")

        result = delete_session_by_id(session_id, user_id)
        return success_response(200, result)

    else:
        return error_response(405, "method_not_allowed")

