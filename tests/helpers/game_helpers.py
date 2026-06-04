def build_game_body(
    game_name="Glacier Gold",
    game_type="slot",
    cash_in=100.00,
    cash_out=None,
    started_at="2026-05-13T05:02:00Z",
    ended_at=None,
    notes="Dime denom - 2.00 spins",
    entry_mode=None,
    freeplay_used=None
    ):
    # helper function to create a game for testing purposes
    body = {
        "game_name": game_name,
        "game_type": game_type,
        "cash_in": cash_in,
        "started_at": started_at,
        "notes": notes
    }

    if cash_out is not None:
        body["cash_out"] = cash_out

    if entry_mode is not None:
        body["entry_mode"] = entry_mode

    if ended_at is not None:
        body["ended_at"] = ended_at

    if freeplay_used is not None:
        body["freeplay_used"] = freeplay_used

    return body