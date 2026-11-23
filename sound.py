import math
import struct

import pygame

_enabled = False
_cache = {}

SAMPLE_RATE = 44100


def init_sound():
    global _enabled
    try:
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
        _enabled = True
    except pygame.error:
        _enabled = False


def _tone(frequency, duration_ms, volume=0.3):
    n_samples = int(SAMPLE_RATE * duration_ms / 1000)
    amplitude = int(32767 * volume)
    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        value = amplitude if math.sin(2 * math.pi * frequency * t) >= 0 else -amplitude
        decay = 1 - (i / n_samples)
        samples.append(int(value * decay))
    buffer = struct.pack("<%dh" % n_samples, *samples)
    return pygame.mixer.Sound(buffer=buffer)


def get_hit_sound():
    if not _enabled:
        return None
    if "hit" not in _cache:
        _cache["hit"] = _tone(140, 90, volume=0.4)
    return _cache["hit"]


def get_block_sound():
    if not _enabled:
        return None
    if "block" not in _cache:
        _cache["block"] = _tone(300, 60, volume=0.25)
    return _cache["block"]


def get_round_end_sound():
    if not _enabled:
        return None
    if "round_end" not in _cache:
        _cache["round_end"] = _tone(520, 220, volume=0.3)
    return _cache["round_end"]


def play(sound):
    if sound is not None:
        sound.play()
