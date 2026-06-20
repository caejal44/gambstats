interface CreateTripRequest {
    tripName: string;
    location: string;
    tripBudget: number;
    startedAt: string;
    notes: string;
}

interface CreateTripResponse {
    trip_id: string;
    user_id: string;
    trip_name: string;
    location: string;
    trip_budget: number;
    started_at: string;
    ended_at: string | null;
    created_at: string;
    status: string;
    notes: string | null;
}

export async function createTrip(
    payload: CreateTripRequest
): Promise<CreateTripResponse> {

    const API_URL = "/trips";

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

    const data: CreateTripResponse = await response.json();

    return data;
}