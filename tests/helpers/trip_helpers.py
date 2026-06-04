def build_trip_body(
    trip_name="Vegas Test Trip",
    location="Las Vegas",
    trip_budget=1000,
    started_at="2026-05-13T05:00:00Z",
    ended_at=None,
    notes="Test Trip"
    ):
    # helper function to create a trip for testing purposes
    body = {
        "trip_name": trip_name,
        "location": location,
        "trip_budget": trip_budget,
        "started_at": started_at,
        "notes": notes
    }

    if ended_at is not None:
        body["ended_at"] = ended_at

    return body


