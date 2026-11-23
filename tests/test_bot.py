import random

from bot import Bot
from fighter import CONTROLS_P1, CONTROLS_P2, Fighter


def test_bot_approaches_when_far_from_opponent():
    random.seed(0)
    player = Fighter(50, 1, (210, 60, 60), CONTROLS_P1, "P1")
    cpu = Fighter(700, -1, (60, 90, 210), CONTROLS_P2, "CPU")
    bot = Bot("medio")

    for _ in range(300):
        bot._decide(cpu, player)
        cpu.set_horizontal(bot.move_dir * 5)

    assert cpu.rect.x < 700


def test_bot_attacks_when_in_range_eventually():
    random.seed(1)
    player = Fighter(300, 1, (210, 60, 60), CONTROLS_P1, "P1")
    cpu = Fighter(340, -1, (60, 90, 210), CONTROLS_P2, "CPU")
    bot = Bot("dificil")

    punched = False
    for _ in range(300):
        bot._decide(cpu, player)
        if cpu.attack_active > 0:
            punched = True
        cpu.update(player)
        player.update(cpu)

    assert punched


def test_bot_blocks_when_opponent_attacks_nearby():
    random.seed(2)
    player = Fighter(300, 1, (210, 60, 60), CONTROLS_P1, "P1")
    cpu = Fighter(340, -1, (60, 90, 210), CONTROLS_P2, "CPU")
    bot = Bot("dificil")
    player.attack_active = 8  # simulate an ongoing attack from the player

    blocked_at_least_once = False
    for _ in range(200):
        bot._decide(cpu, player)
        if bot.want_block:
            blocked_at_least_once = True

    assert blocked_at_least_once


def test_higher_difficulty_reacts_faster():
    easy = Bot("facil")
    hard = Bot("dificil")
    assert hard.params["reaction_ms"] < easy.params["reaction_ms"]


def test_higher_difficulty_attacks_more_aggressively():
    easy = Bot("facil")
    hard = Bot("dificil")
    assert hard.params["attack_prob"] > easy.params["attack_prob"]
