def build_session_body(
    casino="Aria",
    started_at="2026-05-13T05:00:00Z",
    ended_at=None,
    notes="Test Session"
    ):
    # helper function to create a session for testing purposes
    body = {
        "casino": casino,
        "started_at": started_at,
        "notes": notes
    }

    if ended_at is not None:
        body["ended_at"] = ended_at

    return body