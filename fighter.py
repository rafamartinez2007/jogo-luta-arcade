import pygame

WIDTH = 800
HEIGHT = 450
GROUND_Y = 380

FIGHTER_WIDTH = 50
FIGHTER_HEIGHT = 90

GRAVITY = 1.2
JUMP_SPEED = -18
MOVE_SPEED = 5

ATTACK_REACH = 55
ATTACK_ACTIVE_FRAMES = 8
ATTACK_COOLDOWN_FRAMES = 28
DAMAGE_HIT = 8
DAMAGE_BLOCKED = 2
KNOCKBACK = 10

MAX_HEALTH = 100

CONTROLS_P1 = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_w,
    "block": pygame.K_s,
    "punch": pygame.K_SPACE,
}
CONTROLS_P2 = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "jump": pygame.K_UP,
    "block": pygame.K_DOWN,
    "punch": pygame.K_RCTRL,
}


class Fighter:
    def __init__(self, x, facing, color, controls, name):
        self.rect = pygame.Rect(x, GROUND_Y - FIGHTER_HEIGHT, FIGHTER_WIDTH, FIGHTER_HEIGHT)
        self.vel_y = 0
        self.facing = facing
        self.color = color
        self.controls = controls
        self.name = name
        self.health = MAX_HEALTH
        self.on_ground = True
        self.blocking = False
        self.attack_cooldown = 0
        self.attack_active = 0
        self.hit_registered = False

    def reset(self, x, facing):
        self.rect.x = x
        self.rect.y = GROUND_Y - FIGHTER_HEIGHT
        self.vel_y = 0
        self.facing = facing
        self.health = MAX_HEALTH
        self.on_ground = True
        self.blocking = False
        self.attack_cooldown = 0
        self.attack_active = 0
        self.hit_registered = False

    def handle_keydown(self, key):
        if key == self.controls["jump"] and self.on_ground:
            self.vel_y = JUMP_SPEED
            self.on_ground = False
        if key == self.controls["punch"] and self.attack_cooldown <= 0:
            self.attack_active = ATTACK_ACTIVE_FRAMES
            self.attack_cooldown = ATTACK_COOLDOWN_FRAMES
            self.hit_registered = False

    def handle_keys(self, keys):
        move = 0
        if keys[self.controls["left"]]:
            move -= MOVE_SPEED
        if keys[self.controls["right"]]:
            move += MOVE_SPEED
        self.rect.x += move
        self.rect.x = max(0, min(WIDTH - FIGHTER_WIDTH, self.rect.x))

        self.blocking = keys[self.controls["block"]] and self.on_ground

    def update(self, opponent):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

        if self.rect.centerx < opponent.rect.centerx:
            self.facing = 1
        else:
            self.facing = -1

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_active > 0:
            self.attack_active -= 1
            if not self.hit_registered:
                hitbox = self.get_hitbox()
                if hitbox.colliderect(opponent.rect):
                    self.hit_registered = True
                    facing_each_other = opponent.facing == -self.facing
                    if opponent.blocking and facing_each_other:
                        opponent.health -= DAMAGE_BLOCKED
                    else:
                        opponent.health -= DAMAGE_HIT
                        opponent.rect.x += KNOCKBACK * self.facing
                        opponent.rect.x = max(
                            0, min(WIDTH - FIGHTER_WIDTH, opponent.rect.x)
                        )
                    opponent.health = max(0, opponent.health)

    def get_hitbox(self):
        if self.facing == 1:
            return pygame.Rect(
                self.rect.right, self.rect.centery - 8, ATTACK_REACH, 16
            )
        return pygame.Rect(
            self.rect.left - ATTACK_REACH, self.rect.centery - 8, ATTACK_REACH, 16
        )

    def draw(self, window):
        body_color = self.color
        if self.blocking:
            body_color = tuple(min(255, c + 60) for c in self.color)

        pygame.draw.rect(window, body_color, self.rect, border_radius=6)

        head_center = (self.rect.centerx, self.rect.top - 14)
        pygame.draw.circle(window, (255, 219, 172), head_center, 16)

        if self.attack_active > 0:
            hitbox = self.get_hitbox()
            arm_end = (hitbox.right, hitbox.centery) if self.facing == 1 else (
                hitbox.left,
                hitbox.centery,
            )
            pygame.draw.line(
                window, (255, 230, 120), (self.rect.centerx, self.rect.centery), arm_end, 6
            )

        if self.blocking:
            shield_x = self.rect.right if self.facing == 1 else self.rect.left - 10
            pygame.draw.rect(
                window, (120, 180, 255), (shield_x, self.rect.top, 10, self.rect.height)
            )


def draw_health_bar(window, font, fighter, x, align_right=False):
    bar_width = 260
    bar_height = 22
    y = 20
    bar_x = x if not align_right else x - bar_width
    pygame.draw.rect(window, (60, 60, 60), (bar_x, y, bar_width, bar_height), border_radius=4)
    fill = int(bar_width * fighter.health / MAX_HEALTH)
    fill_x = bar_x if not align_right else bar_x + bar_width - fill
    color = (90, 200, 90) if fighter.health > 35 else (220, 70, 70)
    pygame.draw.rect(window, color, (fill_x, y, fill, bar_height), border_radius=4)
    pygame.draw.rect(window, (20, 20, 20), (bar_x, y, bar_width, bar_height), 2, border_radius=4)
    label = font.render(fighter.name, True, (30, 30, 30))
    label_x = bar_x if not align_right else bar_x + bar_width - label.get_width()
    window.blit(label, (label_x, y + bar_height + 2))


def draw_round_score(window, font, p1_wins, p2_wins, rounds_to_win):
    for i in range(rounds_to_win):
        cx = WIDTH // 2 - 30 + i * 22
        color = (220, 60, 60) if i < p1_wins else (90, 90, 90)
        pygame.draw.circle(window, color, (cx, 30), 7)
    for i in range(rounds_to_win):
        cx = WIDTH // 2 + 30 - i * 22
        color = (60, 90, 220) if i < p2_wins else (90, 90, 90)
        pygame.draw.circle(window, color, (cx, 30), 7)
