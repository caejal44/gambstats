import json

from src.common.responses import success_response, error_response
from src.common.utils import get_required_path_param, get_current_user_id, error_handler
from src.games.schemas import CreateGameRequest, UpdateGameRequest
from src.games.service import create_game, show_game_by_id, show_games_by_session, modify_game, delete_game_by_id

@error_handler
def lambda_handler(event, context):
    method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")

    user_id = get_current_user_id(event)

    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        request = CreateGameRequest(**body)
        session_id = get_required_path_param(event, "session_id")
        game = create_game(request, user_id, session_id)
        return success_response(201, game.model_dump())

    elif method == "GET":
        # GET supports both list and detail views:
        # /games and /games/{game_id}
        path_params = event.get("pathParameters") or {}
        game_id = path_params.get("game_id")

        if game_id:
            game = show_game_by_id(game_id, user_id)
            return success_response(200, game.model_dump())

        session_id = get_required_path_param(event, "session_id")
        games = show_games_by_session(session_id, user_id)
        return success_response(200, games.model_dump())

    elif method == "PATCH":
        # PATCH and DELETE require a specific game_id.
        game_id = get_required_path_param(event, "game_id")
        body = json.loads(event.get("body") or "{}")
        request = UpdateGameRequest(**body)
        game = modify_game(request, game_id, user_id)
        return success_response(200, game.model_dump())

    elif method == "DELETE":
        game_id = get_required_path_param(event, "game_id")

        result = delete_game_by_id(game_id, user_id)
        return success_response(200, result)

    else:
        return error_response(405, "method_not_allowed")