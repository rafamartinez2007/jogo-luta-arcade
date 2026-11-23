import pygame

import main as m


def test_new_menu_state_starts_at_mode_selection():
    menu = m.new_menu_state()
    assert menu["status"] == "menu_mode"
    assert menu["mode"] is None
    assert menu["difficulty"] is None


def test_draw_menu_mode_does_not_crash():
    window = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 44)
    m.draw_menu_mode(window, big_font, font)


def test_draw_menu_difficulty_does_not_crash():
    window = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 44)
    m.draw_menu_difficulty(window, big_font, font)


def test_draw_menu_ready_does_not_crash_for_2p():
    window = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 44)
    menu = {"status": "menu_ready", "mode": "2p", "difficulty": None}
    m.draw_menu_ready(window, big_font, font, menu)


def test_draw_menu_ready_does_not_crash_for_cpu():
    window = pygame.display.get_surface()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 44)
    menu = {"status": "menu_ready", "mode": "cpu", "difficulty": "dificil"}
    m.draw_menu_ready(window, big_font, font, menu)
