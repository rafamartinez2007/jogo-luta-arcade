import sys

import pygame

import sound
from bot import DIFFICULTIES, Bot
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

DIFFICULTY_ORDER = ["facil", "medio", "dificil"]


def new_menu_state():
    return {"status": "menu_mode", "mode": None, "difficulty": None}


def build_match(mode, difficulty):
    p1 = Fighter(P1_START_X, 1, (210, 60, 60), CONTROLS_P1, "Jogador 1")
    p2_name = "Computador" if mode == "cpu" else "Jogador 2"
    p2 = Fighter(P2_START_X, -1, (60, 90, 210), CONTROLS_P2, p2_name)
    return {
        "mode": mode,
        "difficulty": difficulty,
        "bot": Bot(difficulty) if mode == "cpu" else None,
        "p1": p1,
        "p2": p2,
        "p1_wins": 0,
        "p2_wins": 0,
        "round_start_ticks": pygame.time.get_ticks(),
        "round_end_ticks": 0,
        "status": "fight",
        "message": "",
        "paused": False,
        "pause_started_at": None,
        "last_remaining": ROUND_SECONDS,
    }


def toggle_pause(state):
    if state["status"] != "fight":
        return
    if not state["paused"]:
        state["paused"] = True
        state["pause_started_at"] = pygame.time.get_ticks()
    else:
        paused_for = pygame.time.get_ticks() - state["pause_started_at"]
        state["round_start_ticks"] += paused_for
        state["paused"] = False
        state["pause_started_at"] = None


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


def draw_menu_mode(window, big_font, font):
    window.fill((235, 235, 245))
    title = big_font.render("Jogo de Luta Arcade", True, (40, 40, 40))
    window.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

    opt1 = font.render("1 - Dois jogadores (mesmo teclado)", True, (60, 60, 60))
    opt2 = font.render("2 - Jogador vs Computador", True, (60, 60, 60))
    window.blit(opt1, opt1.get_rect(center=(WIDTH // 2, 200)))
    window.blit(opt2, opt2.get_rect(center=(WIDTH // 2, 240)))

    hint = font.render("Pressione 1 ou 2  |  ESC sai", True, (110, 110, 110))
    window.blit(hint, hint.get_rect(center=(WIDTH // 2, 320)))


def draw_menu_difficulty(window, big_font, font):
    window.fill((235, 235, 245))
    title = big_font.render("Escolha a dificuldade", True, (40, 40, 40))
    window.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

    for i, key in enumerate(DIFFICULTY_ORDER):
        label = f"{i + 1} - {DIFFICULTIES[key]['label']}"
        opt = font.render(label, True, (60, 60, 60))
        window.blit(opt, opt.get_rect(center=(WIDTH // 2, 190 + i * 40)))

    hint = font.render("Pressione 1, 2 ou 3  |  ESC sai", True, (110, 110, 110))
    window.blit(hint, hint.get_rect(center=(WIDTH // 2, 330)))


def draw_menu_ready(window, big_font, font, menu):
    window.fill((235, 235, 245))
    title = big_font.render("Controles", True, (40, 40, 40))
    window.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

    lines = ["Jogador 1: A/D mover, W pular, S bloquear, ESPACO socar"]
    if menu["mode"] == "2p":
        lines.append(
            "Jogador 2: setas mover/pular, seta p/ baixo bloquear, CTRL direito socar"
        )
    else:
        lines.append(f"Computador no nivel: {DIFFICULTIES[menu['difficulty']]['label']}")
    lines.append("")
    lines.append("P pausa  |  R revanche  |  M menu  |  ESC sai")
    lines.append("Melhor de 3 rounds, 60 segundos cada")

    for i, line in enumerate(lines):
        label = font.render(line, True, (60, 60, 60))
        window.blit(label, label.get_rect(center=(WIDTH // 2, 150 + i * 34)))

    hint = font.render("Pressione ENTER para comecar  |  M volta ao menu", True, (110, 110, 110))
    window.blit(hint, hint.get_rect(center=(WIDTH // 2, 150 + len(lines) * 34 + 20)))


def main():
    pygame.init()
    sound.init_sound()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo de Luta Arcade")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 44)
    hint_font = pygame.font.SysFont(None, 22)

    menu = new_menu_state()
    state = None
    game = True

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = False
                    continue

                if state is None:
                    if menu["status"] == "menu_mode":
                        if event.key == pygame.K_1:
                            menu["mode"] = "2p"
                            menu["status"] = "menu_ready"
                        elif event.key == pygame.K_2:
                            menu["mode"] = "cpu"
                            menu["status"] = "menu_difficulty"
                    elif menu["status"] == "menu_difficulty":
                        chosen = None
                        if event.key == pygame.K_1:
                            chosen = "facil"
                        elif event.key == pygame.K_2:
                            chosen = "medio"
                        elif event.key == pygame.K_3:
                            chosen = "dificil"
                        if chosen:
                            menu["difficulty"] = chosen
                            menu["status"] = "menu_ready"
                    elif menu["status"] == "menu_ready":
                        if event.key == pygame.K_RETURN:
                            state = build_match(menu["mode"], menu["difficulty"])
                        elif event.key == pygame.K_m:
                            menu = new_menu_state()
                else:
                    if event.key == pygame.K_m:
                        state = None
                        menu = new_menu_state()
                    elif event.key == pygame.K_r:
                        state = build_match(state["mode"], state["difficulty"])
                    elif event.key == pygame.K_p:
                        toggle_pause(state)
                    elif state["status"] == "fight" and not state["paused"]:
                        state["p1"].handle_keydown(event.key)
                        if state["mode"] == "2p":
                            state["p2"].handle_keydown(event.key)

        if state is None:
            if menu["status"] == "menu_mode":
                draw_menu_mode(window, big_font, font)
            elif menu["status"] == "menu_difficulty":
                draw_menu_difficulty(window, big_font, font)
            else:
                draw_menu_ready(window, big_font, font, menu)
            pygame.display.update()
            clock.tick(FPS)
            continue

        if state["status"] == "fight" and state["paused"]:
            remaining = state["last_remaining"]
        elif state["status"] == "fight":
            keys = pygame.key.get_pressed()
            state["p1"].handle_keys(keys)
            if state["mode"] == "2p":
                state["p2"].handle_keys(keys)
            else:
                state["bot"].update(state["p2"], state["p1"])

            state["p1"].update(state["p2"])
            state["p2"].update(state["p1"])

            if state["p1"].last_hit_landed or state["p2"].last_hit_landed:
                sound.play(sound.get_hit_sound())
            elif state["p1"].last_hit_blocked or state["p2"].last_hit_blocked:
                sound.play(sound.get_block_sound())

            elapsed = (pygame.time.get_ticks() - state["round_start_ticks"]) / 1000
            remaining = max(0, ROUND_SECONDS - elapsed)
            state["last_remaining"] = remaining

            if state["p1"].health <= 0 or state["p2"].health <= 0 or remaining <= 0:
                resolve_round(state)
                sound.play(sound.get_round_end_sound())
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

        if state["mode"] == "cpu":
            diff_label = font.render(
                f"CPU: {DIFFICULTIES[state['difficulty']]['label']}", True, (90, 90, 90)
            )
            window.blit(diff_label, (WIDTH // 2 - diff_label.get_width() // 2, 60))

        if state["status"] == "fight" and state["paused"]:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((255, 255, 255))
            window.blit(overlay, (0, 0))

            msg_surf = big_font.render("PAUSADO", True, (40, 40, 40))
            window.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            hint = hint_font.render("Pressione P para continuar", True, (60, 60, 60))
            window.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

        if state["status"] in ("round_end", "match_end"):
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((255, 255, 255))
            window.blit(overlay, (0, 0))

            msg_surf = big_font.render(state["message"], True, (40, 40, 40))
            window.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            if state["status"] == "match_end":
                hint = hint_font.render(
                    "R para jogar de novo  |  M para o menu  |  ESC para sair",
                    True,
                    (60, 60, 60),
                )
                window.blit(
                    hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
                )

        if state["mode"] == "2p":
            controls_hint = hint_font.render(
                "P1: A/D mover, W pular, S bloquear, ESPACO socar"
                "   |   P2: setas mover/pular/bloquear, CTRL direito socar   |   P pausa",
                True,
                (90, 90, 90),
            )
        else:
            controls_hint = hint_font.render(
                "A/D mover, W pular, S bloquear, ESPACO socar   |   P pausa   M menu   R revanche",
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
