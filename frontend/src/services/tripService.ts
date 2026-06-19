interface CreateTripRequest {
    tripName: string;
    location: string;
    tripBudget: string;
    startedAt: string;
    notes: string;
}

interface CreateTripResponse {
    tripId: string;
    message: string;
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