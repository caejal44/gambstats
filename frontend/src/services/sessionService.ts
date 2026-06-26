interface CreateSessionRequest {
    casino: string;
    startedAt: string;
    notes: string;
}

export interface SessionResponse {
  session_id: string;
  user_id: string;
  trip_id: string;
  casino: string;
  started_at: string;
  ended_at: string | null;
  created_at: string;
  status: string;
  notes: string | null;
}

export interface SessionListResponse {
    sessions: SessionResponse[];
}

export async function createSession(
    payload: CreateSessionRequest
): Promise<SessionResponse> {

    const API_URL = "/sessions";

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

    const data: SessionResponse = await response.json();

    return data;
}
export async function getSessions(): Promise<SessionListResponse> {

    const API_URL = "/sessions";

    const response = await fetch(API_URL, {
        method: "GET",
        headers: {
            "Accept": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: SessionListResponse = await response.json();

    return data;
}