interface CreateSessionRequest {
    casino: string;
    startedAt: string;
    notes: string;
}

interface CreateSessionResponse {
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

export async function createSession(
    payload: CreateSessionRequest
): Promise<CreateSessionResponse> {

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

    const data: CreateSessionResponse = await response.json();

    return data;
}