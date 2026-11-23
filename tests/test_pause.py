import main as m


def test_toggle_pause_sets_paused_true():
    state = m.build_match("2p", None)
    assert state["paused"] is False
    m.toggle_pause(state)
    assert state["paused"] is True
    assert state["pause_started_at"] is not None


def test_toggle_pause_twice_returns_to_unpaused():
    state = m.build_match("2p", None)
    m.toggle_pause(state)
    m.toggle_pause(state)
    assert state["paused"] is False
    assert state["pause_started_at"] is None


def test_toggle_pause_does_nothing_outside_fight_status():
    state = m.build_match("2p", None)
    state["status"] = "round_end"
    m.toggle_pause(state)
    assert state["paused"] is False


def test_unpausing_shifts_round_start_ticks_forward():
    state = m.build_match("2p", None)
    original_start = state["round_start_ticks"]
    m.toggle_pause(state)
    state["pause_started_at"] -= 500  # simulate 500ms having passed while paused
    m.toggle_pause(state)
    assert state["round_start_ticks"] > original_start
