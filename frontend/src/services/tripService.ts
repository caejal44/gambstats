interface CreateTripRequest {
    tripName: string;
    location: string;
    tripBudget: number;
    startedAt: string;
    notes: string;
}

export interface TripResponse {
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

export interface TripListResponse {
    trips: TripResponse[];
}

export async function createTrip(
    payload: CreateTripRequest
): Promise<TripResponse> {

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

    const data: TripResponse = await response.json();

    return data;
}

export async function getTrips(): Promise<TripListResponse> {

    const API_URL = "/trips";

    const response = await fetch(API_URL, {
        method: "GET",
        headers: {
            "Accept": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: TripListResponse = await response.json();

    return data;
}