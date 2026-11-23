import sound


def test_init_sound_does_not_crash():
    sound.init_sound()


def test_get_hit_sound_returns_cached_object():
    sound.init_sound()
    first = sound.get_hit_sound()
    second = sound.get_hit_sound()
    assert first is second


def test_get_block_sound_and_hit_sound_are_different():
    sound.init_sound()
    assert sound.get_hit_sound() is not sound.get_block_sound()


def test_play_with_none_does_not_crash():
    sound.play(None)
