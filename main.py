import pygame
import random
import math
import os

pygame.init()

# ============================================================
# WINDOW
# ============================================================

WIDTH = 1100
HEIGHT = 720

TOP_BAR = 82
BOTTOM_BAR = 48
CELL = 24

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake")
clock = pygame.time.Clock()

# ============================================================
# FONTS
# ============================================================

FONT_SMALL = pygame.font.Font(None, 24)
FONT = pygame.font.Font(None, 32)
FONT_MEDIUM = pygame.font.Font(None, 42)
FONT_BIG = pygame.font.Font(None, 78)
FONT_HUGE = pygame.font.Font(None, 105)

# ============================================================
# COLORS
# ============================================================

BACKGROUND_TOP = (5, 14, 22)
BACKGROUND_BOTTOM = (8, 28, 34)

PANEL = (10, 27, 34)
PANEL_LIGHT = (16, 42, 48)

GREEN = (66, 225, 115)
GREEN_DARK = (23, 120, 65)
GREEN_LIGHT = (125, 255, 160)

WHITE = (240, 250, 245)
MUTED = (145, 175, 165)

RED = (245, 70, 90)
RED_LIGHT = (255, 130, 145)

GOLD = (255, 205, 70)

CYAN = (70, 220, 230)

BLACK_ALPHA = (0, 0, 0, 150)

# ============================================================
# GAME AREA
# ============================================================

GAME_LEFT = 0
GAME_TOP = TOP_BAR

GAME_WIDTH = WIDTH
GAME_HEIGHT = HEIGHT - TOP_BAR - BOTTOM_BAR

# ============================================================
# HIGH SCORE
# ============================================================

HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read())
        except:
            return 0

    return 0


def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(score))
    except:
        pass


high_score = load_high_score()

# ============================================================
# DIFFICULTY
# ============================================================

DIFFICULTIES = {
    "EASY": 9,
    "NORMAL": 13,
    "HARD": 17
}

difficulty_name = "NORMAL"

# ============================================================
# PARTICLES
# ============================================================


class Particle:

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(TOP_BAR, HEIGHT)
        self.size = random.choice([1, 1, 2, 2, 3])

        self.speed = random.uniform(0.15, 0.5)

        self.alpha = random.randint(30, 100)

    def update(self):

        self.y -= self.speed

        if self.y < TOP_BAR:
            self.y = HEIGHT

    def draw(self):

        surface = pygame.Surface(
            (self.size * 4, self.size * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            surface,
            (60, 210, 170, self.alpha),
            (self.size * 2, self.size * 2),
            self.size
        )

        screen.blit(
            surface,
            (self.x - self.size * 2, self.y - self.size * 2)
        )


particles = [Particle() for _ in range(100)]

# ============================================================
# BACKGROUND
# ============================================================


def create_background():

    background = pygame.Surface((WIDTH, HEIGHT))

    for y in range(HEIGHT):

        progress = y / HEIGHT

        r = int(
            BACKGROUND_TOP[0]
            + (BACKGROUND_BOTTOM[0] - BACKGROUND_TOP[0]) * progress
        )

        g = int(
            BACKGROUND_TOP[1]
            + (BACKGROUND_BOTTOM[1] - BACKGROUND_TOP[1]) * progress
        )

        b = int(
            BACKGROUND_TOP[2]
            + (BACKGROUND_BOTTOM[2] - BACKGROUND_TOP[2]) * progress
        )

        pygame.draw.line(
            background,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )

    # Grid

    for x in range(0, WIDTH, CELL):

        pygame.draw.line(
            background,
            (10, 38, 43),
            (x, TOP_BAR),
            (x, HEIGHT - BOTTOM_BAR)
        )

    for y in range(
        TOP_BAR,
        HEIGHT - BOTTOM_BAR,
        CELL
    ):

        pygame.draw.line(
            background,
            (10, 38, 43),
            (0, y),
            (WIDTH, y)
        )

    return background


BACKGROUND = create_background()

# ============================================================
# TEXT
# ============================================================


def draw_text(
        text,
        font,
        color,
        x,
        y,
        center=False
):

    image = font.render(text, True, color)

    rect = image.get_rect()

    if center:

        rect.center = (x, y)

    else:

        rect.topleft = (x, y)

    screen.blit(image, rect)

# ============================================================
# PANEL
# ============================================================


def draw_panel(rect, color=PANEL):

    shadow = pygame.Surface(
        (rect.width + 12, rect.height + 12),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        shadow,
        (0, 0, 0, 90),
        shadow.get_rect(),
        border_radius=20
    )

    screen.blit(
        shadow,
        (rect.x - 6, rect.y + 6)
    )

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        (30, 80, 78),
        rect,
        width=2,
        border_radius=20
    )

# ============================================================
# FOOD
# ============================================================


def draw_food(food):

    x, y = food

    center = (
        x + CELL // 2,
        y + CELL // 2
    )

    # Glow

    for radius, alpha in [
        (28, 15),
        (23, 25),
        (18, 45)
    ]:

        glow = pygame.Surface(
            (radius * 2, radius * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (245, 70, 90, alpha),
            (radius, radius),
            radius
        )

        screen.blit(
            glow,
            (
                center[0] - radius,
                center[1] - radius
            )
        )

    # Apple

    pygame.draw.circle(
        screen,
        RED,
        center,
        9
    )

    pygame.draw.circle(
        screen,
        RED_LIGHT,
        (
            center[0] - 3,
            center[1] - 3
        ),
        3
    )

    # Leaf

    pygame.draw.ellipse(
        screen,
        GREEN,
        (
            center[0] + 3,
            center[1] - 12,
            10,
            6
        )
    )

    pygame.draw.line(
        screen,
        GREEN_DARK,
        (
            center[0],
            center[1] - 7
        ),
        (
            center[0] + 5,
            center[1] - 13
        ),
        2
    )

# ============================================================
# SNAKE
# ============================================================


def draw_snake(snake, direction):

    for index, (x, y) in enumerate(snake):

        rect = pygame.Rect(
            x + 2,
            y + 2,
            CELL - 4,
            CELL - 4
        )

        if index == 0:

            # Head

            pygame.draw.rect(
                screen,
                GREEN,
                rect,
                border_radius=9
            )

            pygame.draw.rect(
                screen,
                GREEN_LIGHT,
                rect,
                width=2,
                border_radius=9
            )

            # Eyes

            if direction == (1, 0):

                eye1 = (x + 17, y + 7)
                eye2 = (x + 17, y + 16)

            elif direction == (-1, 0):

                eye1 = (x + 7, y + 7)
                eye2 = (x + 7, y + 16)

            elif direction == (0, -1):

                eye1 = (x + 7, y + 7)
                eye2 = (x + 16, y + 7)

            else:

                eye1 = (x + 7, y + 16)
                eye2 = (x + 16, y + 16)

            pygame.draw.circle(
                screen,
                WHITE,
                eye1,
                4
            )

            pygame.draw.circle(
                screen,
                WHITE,
                eye2,
                4
            )

            pygame.draw.circle(
                screen,
                (10, 25, 20),
                eye1,
                2
            )

            pygame.draw.circle(
                screen,
                (10, 25, 20),
                eye2,
                2
            )

        else:

            # Body

            color_factor = max(
                0,
                1 - index / max(len(snake), 1)
            )

            body_color = (
                int(35 + 30 * color_factor),
                int(150 + 55 * color_factor),
                int(75 + 40 * color_factor)
            )

            pygame.draw.rect(
                screen,
                body_color,
                rect,
                border_radius=7
            )

            pygame.draw.rect(
                screen,
                GREEN_DARK,
                rect,
                width=1,
                border_radius=7
            )

            # Scale detail

            pygame.draw.circle(
                screen,
                GREEN_LIGHT,
                (
                    x + 8,
                    y + 8
                ),
                2
            )

# ============================================================
# RANDOM FOOD POSITION
# ============================================================


def random_food(snake):

    cols = WIDTH // CELL

    rows = GAME_HEIGHT // CELL

    while True:

        position = (
            random.randrange(cols) * CELL,
            GAME_TOP
            + random.randrange(rows) * CELL
        )

        if position not in snake:

            return position

# ============================================================
# RESET
# ============================================================


def reset_game():

    center_x = (
        WIDTH // 2 // CELL
    ) * CELL

    center_y = (
        GAME_TOP
        + (GAME_HEIGHT // 2 // CELL) * CELL
    )

    snake = [
        (center_x, center_y),
        (center_x - CELL, center_y),
        (center_x - CELL * 2, center_y),
        (center_x - CELL * 3, center_y)
    ]

    food = random_food(snake)

    direction = (1, 0)

    score = 0

    return (
        snake,
        food,
        direction,
        score
    )

# ============================================================
# MENU
# ============================================================


def main_menu():

    global difficulty_name

    selected = 1

    while True:

        clock.tick(60)

        for particle in particles:
            particle.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    selected -= 1

                    if selected < 0:
                        selected = 3

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s
                ):

                    selected += 1

                    if selected > 3:
                        selected = 0

                elif event.key == pygame.K_RETURN:

                    if selected == 0:

                        return True

                    elif selected == 1:

                        difficulty_name = "EASY"

                    elif selected == 2:

                        difficulty_name = "NORMAL"

                    elif selected == 3:

                        difficulty_name = "HARD"

                elif event.key == pygame.K_ESCAPE:

                    pygame.quit()
                    return False

        screen.blit(
            BACKGROUND,
            (0, 0)
        )

        for particle in particles:
            particle.draw()

        # Logo

        draw_text(
            "NEON",
            FONT_HUGE,
            GREEN,
            WIDTH // 2,
            135,
            center=True
        )

        draw_text(
            "SNAKE",
            FONT_HUGE,
            WHITE,
            WIDTH // 2,
            220,
            center=True
        )

        draw_text(
            "A modern classic",
            FONT,
            MUTED,
            WIDTH // 2,
            275,
            center=True
        )

        menu_rect = pygame.Rect(
            WIDTH // 2 - 220,
            320,
            440,
            260
        )

        draw_panel(menu_rect)

        options = [
            "START GAME",
            "EASY",
            "NORMAL",
            "HARD"
        ]

        for i, option in enumerate(options):

            y = 350 + i * 52

            selected_color = (
                GREEN
                if i == selected
                else WHITE
            )

            draw_text(
                (
                    "▶  " + option
                    if i == selected
                    else option
                ),
                FONT_MEDIUM if i == 0 else FONT,
                selected_color,
                WIDTH // 2,
                y,
                center=True
            )

        draw_text(
            f"Current difficulty: {difficulty_name}",
            FONT_SMALL,
            GOLD,
            WIDTH // 2,
            600,
            center=True
        )

        draw_text(
            "↑ ↓ Select     ENTER Confirm     ESC Quit",
            FONT_SMALL,
            MUTED,
            WIDTH // 2,
            650,
            center=True
        )

        pygame.display.flip()

# ============================================================
# GAME
# ============================================================


def play_game():

    global high_score

    snake, food, direction, score = reset_game()

    game_over = False
    paused = False

    last_move = pygame.time.get_ticks()

    while True:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:

                # --------------------------
                # Game Over
                # --------------------------

                if game_over:

                    if event.key == pygame.K_RETURN:

                        return True

                    if event.key == pygame.K_ESCAPE:

                        return False

                    continue

                # --------------------------
                # Pause
                # --------------------------

                if event.key == pygame.K_p:

                    paused = not paused

                elif event.key == pygame.K_ESCAPE:

                    return False

                elif event.key == pygame.K_r:

                    snake, food, direction, score = reset_game()

                    paused = False
                    game_over = False

                # --------------------------
                # Movement
                # --------------------------

                elif event.key in (
                    pygame.K_UP,
                    pygame.K_w
                ):

                    if direction != (0, 1):
                        direction = (0, -1)

                elif event.key in (
                    pygame.K_DOWN,
                    pygame.K_s
                ):

                    if direction != (0, -1):
                        direction = (0, 1)

                elif event.key in (
                    pygame.K_LEFT,
                    pygame.K_a
                ):

                    if direction != (1, 0):
                        direction = (-1, 0)

                elif event.key in (
                    pygame.K_RIGHT,
                    pygame.K_d
                ):

                    if direction != (-1, 0):
                        direction = (1, 0)

        # ====================================================
        # UPDATE GAME
        # ====================================================

        if not paused and not game_over:

            current_time = pygame.time.get_ticks()

            base_speed = DIFFICULTIES[difficulty_name]

            # Speed increases as player scores

            speed_bonus = min(
                score // 50,
                8
            )

            speed = base_speed + speed_bonus

            move_delay = 1000 / speed

            if current_time - last_move >= move_delay:

                last_move = current_time

                head_x, head_y = snake[0]

                new_head = (
                    head_x + direction[0] * CELL,
                    head_y + direction[1] * CELL
                )

                left = 0
                right = WIDTH - CELL

                top = GAME_TOP
                bottom = HEIGHT - BOTTOM_BAR - CELL

                # Wall collision

                if (
                    new_head[0] < left
                    or new_head[0] > right
                    or new_head[1] < top
                    or new_head[1] > bottom
                ):

                    game_over = True

                # Snake collision

                elif new_head in snake:

                    game_over = True

                else:

                    snake.insert(
                        0,
                        new_head
                    )

                    # Food eaten

                    if new_head == food:

                        score += 10

                        if score > high_score:

                            high_score = score
                            save_high_score(high_score)

                        food = random_food(
                            snake
                        )

                    else:

                        snake.pop()

        # ====================================================
        # BACKGROUND
        # ====================================================

        screen.blit(
            BACKGROUND,
            (0, 0)
        )

        # Animated particles

        for particle in particles:

            particle.update()
            particle.draw()

        # ====================================================
        # TOP BAR
        # ====================================================

        pygame.draw.rect(
            screen,
            (7, 22, 29),
            (0, 0, WIDTH, TOP_BAR)
        )

        pygame.draw.line(
            screen,
            (35, 105, 85),
            (0, TOP_BAR),
            (WIDTH, TOP_BAR),
            2
        )

        draw_text(
            "NEON SNAKE",
            FONT_MEDIUM,
            GREEN,
            25,
            20
        )

        # Score panel

        draw_text(
            "SCORE",
            FONT_SMALL,
            MUTED,
            530,
            15
        )

        draw_text(
            str(score),
            FONT_MEDIUM,
            WHITE,
            530,
            34
        )

        # High score

        draw_text(
            "BEST",
            FONT_SMALL,
            MUTED,
            650,
            15
        )

        draw_text(
            str(high_score),
            FONT_MEDIUM,
            GOLD,
            650,
            34
        )

        # Length

        draw_text(
            "LENGTH",
            FONT_SMALL,
            MUTED,
            770,
            15
        )

        draw_text(
            str(len(snake)),
            FONT_MEDIUM,
            CYAN,
            770,
            34
        )

        # Difficulty

        draw_text(
            difficulty_name,
            FONT,
            GREEN_LIGHT,
            930,
            28
        )

        # ====================================================
        # GAME
        # ====================================================

        draw_food(food)

        draw_snake(
            snake,
            direction
        )

        # ====================================================
        # BOTTOM BAR
        # ====================================================

        pygame.draw.rect(
            screen,
            (7, 22, 29),
            (
                0,
                HEIGHT - BOTTOM_BAR,
                WIDTH,
                BOTTOM_BAR
            )
        )

        draw_text(
            "WASD / ARROWS  MOVE",
            FONT_SMALL,
            MUTED,
            20,
            HEIGHT - 34
        )

        draw_text(
            "P  PAUSE",
            FONT_SMALL,
            MUTED,
            360,
            HEIGHT - 34
        )

        draw_text(
            "R  RESTART",
            FONT_SMALL,
            MUTED,
            490,
            HEIGHT - 34
        )

        draw_text(
            "ESC  MENU",
            FONT_SMALL,
            MUTED,
            640,
            HEIGHT - 34
        )

        # ====================================================
        # PAUSE
        # ====================================================

        if paused and not game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 160)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            pause_panel = pygame.Rect(
                WIDTH // 2 - 250,
                HEIGHT // 2 - 140,
                500,
                280
            )

            draw_panel(
                pause_panel
            )

            draw_text(
                "PAUSED",
                FONT_BIG,
                GREEN,
                WIDTH // 2,
                HEIGHT // 2 - 65,
                center=True
            )

            draw_text(
                "Take a break",
                FONT,
                MUTED,
                WIDTH // 2,
                HEIGHT // 2,
                center=True
            )

            draw_text(
                "Press P to continue",
                FONT_SMALL,
                WHITE,
                WIDTH // 2,
                HEIGHT // 2 + 65,
                center=True
            )

        # ====================================================
        # GAME OVER
        # ====================================================

        if game_over:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 175)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            panel = pygame.Rect(
                WIDTH // 2 - 300,
                HEIGHT // 2 - 190,
                600,
                380
            )

            draw_panel(
                panel,
                (11, 27, 34)
            )

            draw_text(
                "GAME OVER",
                FONT_BIG,
                RED,
                WIDTH // 2,
                HEIGHT // 2 - 110,
                center=True
            )

            draw_text(
                "Your snake has crashed!",
                FONT,
                MUTED,
                WIDTH // 2,
                HEIGHT // 2 - 55,
                center=True
            )

            draw_text(
                f"SCORE   {score}",
                FONT_MEDIUM,
                WHITE,
                WIDTH // 2,
                HEIGHT // 2 + 5,
                center=True
            )

            if score == high_score and score > 0:

                draw_text(
                    "★ NEW HIGH SCORE ★",
                    FONT,
                    GOLD,
                    WIDTH // 2,
                    HEIGHT // 2 + 55,
                    center=True
                )

            else:

                draw_text(
                    f"BEST   {high_score}",
                    FONT,
                    GOLD,
                    WIDTH // 2,
                    HEIGHT // 2 + 55,
                    center=True
                )

            draw_text(
                "PRESS ENTER TO PLAY AGAIN",
                FONT,
                GREEN,
                WIDTH // 2,
                HEIGHT // 2 + 110,
                center=True
            )

            draw_text(
                "ESC  Return to Menu",
                FONT_SMALL,
                MUTED,
                WIDTH // 2,
                HEIGHT // 2 + 150,
                center=True
            )

        pygame.display.flip()


# ============================================================
# MAIN LOOP
# ============================================================


while True:

    result = main_menu()

    if not result:
        break

    result = play_game()

    if not result:
        break


pygame.quit()