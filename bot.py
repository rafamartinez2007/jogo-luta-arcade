import random

import pygame

from fighter import ATTACK_REACH, FIGHTER_WIDTH, MOVE_SPEED

DIFFICULTIES = {
    "facil": {
        "label": "Facil",
        "reaction_ms": 450,
        "attack_prob": 0.35,
        "block_prob": 0.30,
        "jump_prob": 0.015,
        "approach_bias": 0.55,
    },
    "medio": {
        "label": "Medio",
        "reaction_ms": 250,
        "attack_prob": 0.55,
        "block_prob": 0.55,
        "jump_prob": 0.02,
        "approach_bias": 0.80,
    },
    "dificil": {
        "label": "Dificil",
        "reaction_ms": 120,
        "attack_prob": 0.80,
        "block_prob": 0.80,
        "jump_prob": 0.025,
        "approach_bias": 0.95,
    },
}


class Bot:
    def __init__(self, difficulty="medio"):
        self.difficulty = difficulty
        self.params = DIFFICULTIES[difficulty]
        self.next_decision = 0
        self.move_dir = 0
        self.want_block = False

    def update(self, fighter, opponent):
        now = pygame.time.get_ticks()
        if now >= self.next_decision:
            self._decide(fighter, opponent)
            self.next_decision = now + self.params["reaction_ms"]

        fighter.set_horizontal(self.move_dir * MOVE_SPEED)
        fighter.blocking = self.want_block and fighter.on_ground

    def _decide(self, fighter, opponent):
        p = self.params
        distance = opponent.rect.centerx - fighter.rect.centerx
        abs_distance = abs(distance)
        ideal_range = ATTACK_REACH + FIGHTER_WIDTH // 2 + 5

        if abs_distance > ideal_range + 20:
            self.move_dir = 1 if distance > 0 else -1
        elif abs_distance < ideal_range - 15 and random.random() > p["approach_bias"]:
            self.move_dir = -1 if distance > 0 else 1
        else:
            self.move_dir = 0

        if (
            opponent.attack_active > 0
            and abs_distance < ideal_range + 20
            and random.random() < p["block_prob"]
        ):
            self.want_block = True
            return

        self.want_block = False

        if (
            abs_distance <= ideal_range
            and fighter.attack_cooldown <= 0
            and random.random() < p["attack_prob"]
        ):
            fighter.try_punch()

        if random.random() < p["jump_prob"]:
            fighter.try_jump()
