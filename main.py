import sys

import pygame

from fighter import (
    CONTROLS_P1,
    CONTROLS_P2,
    FIGHTER_WIDTH,
    GROUND_Y,
    HEIGHT,
    WIDTH,
    Fighter,
    draw_health_bar,
    draw_round_score,
)

FPS = 60
ROUND_SECONDS = 60
ROUNDS_TO_WIN = 2
ROUND_END_DISPLAY_MS = 2200

P1_START_X = 150
P2_START_X = WIDTH - 150 - FIGHTER_WIDTH


def new_match_state():
    p1 = Fighter(P1_START_X, 1, (210, 60, 60), CONTROLS_P1, "Jogador 1")
    p2 = Fighter(P2_START_X, -1, (60, 90, 210), CONTROLS_P2, "Jogador 2")
    return {
        "p1": p1,
        "p2": p2,
        "p1_wins": 0,
        "p2_wins": 0,
        "round_start_ticks": pygame.time.get_ticks(),
        "round_end_ticks": 0,
        "status": "fight",  # fight, round_end, match_end
        "message": "",
    }


def start_next_round(state):
    state["p1"].reset(P1_START_X, 1)
    state["p2"].reset(P2_START_X, -1)
    state["round_start_ticks"] = pygame.time.get_ticks()
    state["status"] = "fight"


def resolve_round(state):
    p1, p2 = state["p1"], state["p2"]
    if p1.health <= 0 and p2.health <= 0:
        state["message"] = "Round empatado!"
    elif p1.health <= 0:
        state["p2_wins"] += 1
        state["message"] = f"{p2.name} venceu o round!"
    elif p2.health <= 0:
        state["p1_wins"] += 1
        state["message"] = f"{p1.name} venceu o round!"
    else:
        if p1.health > p2.health:
            state["p1_wins"] += 1
            state["message"] = f"{p1.name} venceu o round no tempo!"
        elif p2.health > p1.health:
            state["p2_wins"] += 1
            state["message"] = f"{p2.name} venceu o round no tempo!"
        else:
            state["message"] = "Round empatado!"

    state["round_end_ticks"] = pygame.time.get_ticks()
    if state["p1_wins"] >= ROUNDS_TO_WIN or state["p2_wins"] >= ROUNDS_TO_WIN:
        winner = state["p1"].name if state["p1_wins"] > state["p2_wins"] else state["p2"].name
        state["message"] = f"{winner} venceu a luta!"
        state["status"] = "match_end"
    else:
        state["status"] = "round_end"


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo de Luta Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 44)
    hint_font = pygame.font.SysFont(None, 22)

    state = new_match_state()
    game = True

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                elif event.key == pygame.K_r:
                    state = new_match_state()
                elif state["status"] == "fight":
                    state["p1"].handle_keydown(event.key)
                    state["p2"].handle_keydown(event.key)

        if state["status"] == "fight":
            keys = pygame.key.get_pressed()
            state["p1"].handle_keys(keys)
            state["p2"].handle_keys(keys)
            state["p1"].update(state["p2"])
            state["p2"].update(state["p1"])

            elapsed = (pygame.time.get_ticks() - state["round_start_ticks"]) / 1000
            remaining = max(0, ROUND_SECONDS - elapsed)

            if state["p1"].health <= 0 or state["p2"].health <= 0 or remaining <= 0:
                resolve_round(state)
        elif state["status"] == "round_end":
            if pygame.time.get_ticks() - state["round_end_ticks"] >= ROUND_END_DISPLAY_MS:
                start_next_round(state)
            remaining = 0
        else:
            remaining = 0

        window.fill((235, 235, 245))
        pygame.draw.rect(window, (200, 170, 140), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        pygame.draw.line(window, (120, 90, 60), (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

        state["p1"].draw(window)
        state["p2"].draw(window)

        draw_health_bar(window, font, state["p1"], 20)
        draw_health_bar(window, font, state["p2"], WIDTH - 20, align_right=True)
        draw_round_score(window, font, state["p1_wins"], state["p2_wins"], ROUNDS_TO_WIN)

        if state["status"] == "fight":
            timer_label = big_font.render(str(int(remaining)), True, (60, 60, 60))
            window.blit(timer_label, timer_label.get_rect(center=(WIDTH // 2, 45)))

        if state["status"] in ("round_end", "match_end"):
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((255, 255, 255))
            window.blit(overlay, (0, 0))

            msg_surf = big_font.render(state["message"], True, (40, 40, 40))
            window.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            if state["status"] == "match_end":
                hint = hint_font.render(
                    "Pressione R para jogar de novo ou ESC para sair", True, (60, 60, 60)
                )
                window.blit(
                    hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
                )

        controls_hint = hint_font.render(
            "P1: A/D mover, W pular, S bloquear, ESPACO socar"
            "   |   P2: setas mover/pular/bloquear, CTRL direito socar",
            True,
            (90, 90, 90),
        )
        window.blit(controls_hint, controls_hint.get_rect(center=(WIDTH // 2, HEIGHT - 12)))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
