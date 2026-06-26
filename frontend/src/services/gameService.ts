interface CreateGameRequest {
 gameName: string;
 gameType: string;
 cashIn: number;
 startedAt: string;
 notes: string;
 freeplayUsed: number;

}

export interface GameResponse {
 game_id: string;
 session_id: string;
 trip_id: string;
 user_id: string;
 game_name: string;
 game_type: string;
 cash_in: number;
 cash_out: number | null;
 started_at: string | null;
 ended_at: string | null;
 created_at: string;
 status: string;
 notes: string | null;
 freeplay_used: number | null;
}

export interface GameListResponse {
    games: GameResponse[];
}

export async function createGame(
    payload: CreateGameRequest
): Promise<GameResponse> {

    const API_URL = "/games";

    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: GameResponse = await response.json();

    return data;
}
export async function getGames(): Promise<GameListResponse> {

    const API_URL = "/games";

    const response = await fetch(API_URL, {
        method: "GET",
        headers: {
            "Accept": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: GameListResponse = await response.json();

    return data;
}