import main as m
from fighter import MAX_HEALTH


def test_resolve_round_ko_awards_point_to_survivor():
    state = m.build_match("2p", None)
    state["p2"].health = 0
    m.resolve_round(state)
    assert state["p1_wins"] == 1
    assert state["p2_wins"] == 0
    assert state["status"] == "round_end"


def test_resolve_round_double_ko_is_a_draw():
    state = m.build_match("2p", None)
    state["p1"].health = 0
    state["p2"].health = 0
    m.resolve_round(state)
    assert state["p1_wins"] == 0
    assert state["p2_wins"] == 0
    assert state["status"] == "round_end"


def test_resolve_round_equal_health_timeout_is_a_draw():
    state = m.build_match("2p", None)
    m.resolve_round(state)
    assert state["p1_wins"] == 0
    assert state["p2_wins"] == 0


def test_resolve_round_higher_health_wins_on_timeout():
    state = m.build_match("2p", None)
    state["p2"].health = 50
    m.resolve_round(state)
    assert state["p1_wins"] == 1
    assert state["p2_wins"] == 0


def test_match_ends_after_reaching_rounds_to_win():
    state = m.build_match("2p", None)
    state["p1_wins"] = m.ROUNDS_TO_WIN - 1
    state["p2"].health = 0
    m.resolve_round(state)
    assert state["status"] == "match_end"
    assert "Jogador 1" in state["message"]


def test_start_next_round_resets_fighters_but_keeps_score():
    state = m.build_match("2p", None)
    state["p1"].health = 10
    state["p1_wins"] = 1
    m.start_next_round(state)
    assert state["p1"].health == MAX_HEALTH
    assert state["status"] == "fight"
    assert state["p1_wins"] == 1  # score persists across rounds


def test_build_match_cpu_mode_creates_bot():
    state = m.build_match("cpu", "facil")
    assert state["bot"] is not None
    assert state["p2"].name == "Computador"


def test_build_match_2p_mode_has_no_bot():
    state = m.build_match("2p", None)
    assert state["bot"] is None
    assert state["p2"].name == "Jogador 2"
