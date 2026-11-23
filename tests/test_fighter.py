from fighter import (
    CONTROLS_P1,
    CONTROLS_P2,
    DAMAGE_BLOCKED,
    DAMAGE_HIT,
    MAX_HEALTH,
    Fighter,
)


def make_pair(gap=40):
    p1 = Fighter(300, 1, (210, 60, 60), CONTROLS_P1, "P1")
    p2 = Fighter(300 + gap, -1, (60, 90, 210), CONTROLS_P2, "P2")
    return p1, p2


def test_punch_in_range_deals_full_damage():
    p1, p2 = make_pair()
    p1.try_punch()
    p1.update(p2)
    assert p2.health == MAX_HEALTH - DAMAGE_HIT


def test_punch_out_of_range_misses():
    p1, p2 = make_pair(gap=400)
    p1.try_punch()
    p1.update(p2)
    assert p2.health == MAX_HEALTH


def test_blocking_reduces_damage():
    p1, p2 = make_pair()
    p2.blocking = True
    p1.try_punch()
    p1.update(p2)
    assert p2.health == MAX_HEALTH - DAMAGE_BLOCKED


def test_hit_applies_knockback_away_from_attacker():
    p1, p2 = make_pair()
    start_x = p2.rect.x
    p1.try_punch()
    p1.update(p2)
    assert p2.rect.x > start_x


def test_attack_cooldown_blocks_immediate_second_punch():
    p1, p2 = make_pair()
    p1.try_punch()
    assert p1.attack_cooldown > 0
    cooldown_before = p1.attack_cooldown
    p1.try_punch()
    assert p1.attack_cooldown == cooldown_before


def test_single_punch_only_hits_once():
    p1, p2 = make_pair()
    p1.try_punch()
    for _ in range(8):
        p1.update(p2)
    assert p2.health == MAX_HEALTH - DAMAGE_HIT


def test_jump_only_works_on_ground():
    p1, _ = make_pair()
    p1.try_jump()
    assert p1.on_ground is False
    vel_after_first_jump = p1.vel_y
    p1.try_jump()
    assert p1.vel_y == vel_after_first_jump


def test_unblocked_hit_sets_last_hit_landed_flag():
    p1, p2 = make_pair()
    p1.try_punch()
    p1.update(p2)
    assert p1.last_hit_landed is True
    assert p1.last_hit_blocked is False


def test_blocked_hit_sets_last_hit_blocked_flag():
    p1, p2 = make_pair()
    p2.blocking = True
    p1.try_punch()
    p1.update(p2)
    assert p1.last_hit_blocked is True
    assert p1.last_hit_landed is False


def test_hit_flags_reset_on_frame_without_a_new_hit():
    p1, p2 = make_pair()
    p1.try_punch()
    p1.update(p2)
    assert p1.last_hit_landed is True
    p1.update(p2)
    assert p1.last_hit_landed is False


def test_reset_restores_full_health_and_position():
    p1, p2 = make_pair()
    p1.try_punch()
    p1.update(p2)
    assert p2.health < MAX_HEALTH
    p2.reset(600, -1)
    assert p2.health == MAX_HEALTH
    assert p2.rect.x == 600
