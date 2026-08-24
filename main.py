import pygame
import random
import math
import os

pygame.init()

WIDTH, HEIGHT = 1000, 700
CELL = 25
TOP_BAR = 90
FPS = 12

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake — PyCharm Edition")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 34)
BIG_FONT = pygame.font.Font(None, 74)
SMALL_FONT = pygame.font.Font(None, 25)

GREEN = (65, 210, 105)
DARK_GREEN = (20, 105, 58)
TEXT = (235, 250, 240)
MUTED = (150, 180, 165)
RED = (235, 75, 95)
GOLD = (255, 205, 75)

ASSET = os.path.join(os.path.dirname(__file__), "assets", "snake_head.png")
snake_sprite = pygame.image.load(ASSET).convert_alpha()
snake_sprite = pygame.transform.smoothscale(snake_sprite, (CELL * 2, CELL * 2))

def make_background():
    bg = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        t = y / HEIGHT
        c = (
            int(7 + 4*t),
            int(18 + 14*t),
            int(27 + 16*t)
        )
        pygame.draw.line(bg, c, (0, y), (WIDTH, y))

    # soft grid
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(bg, (14, 39, 44), (x, TOP_BAR), (x, HEIGHT))
    for y in range(TOP_BAR, HEIGHT, CELL):
        pygame.draw.line(bg, (14, 39, 44), (0, y), (WIDTH, y))

    # decorative glowing dots
    random.seed(10)
    for _ in range(80):
        x = random.randrange(WIDTH)
        y = random.randrange(TOP_BAR, HEIGHT)
        r = random.choice([1, 1, 2, 3])
        pygame.draw.circle(bg, (22, 66, 65), (x, y), r)

    return bg

BACKGROUND = make_background()

def draw_text(surface, text, font, color, pos, center=False):
    s = font.render(text, True, color)
    rect = s.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(s, rect)

def random_food(snake):
    cols = WIDTH // CELL
    rows = (HEIGHT - TOP_BAR) // CELL
    while True:
        p = (random.randrange(cols) * CELL, TOP_BAR + random.randrange(rows) * CELL)
        if p not in snake:
            return p

def reset_game():
    center_x = (WIDTH // 2 // CELL) * CELL
    center_y = TOP_BAR + ((HEIGHT - TOP_BAR) // 2 // CELL) * CELL
    snake = [
        (center_x, center_y),
        (center_x - CELL, center_y),
        (center_x - 2*CELL, center_y),
    ]
    return snake, (CELL, TOP_BAR + CELL), (1, 0), 0, False

snake, food, direction, score, game_over = reset_game()
best_score = 0
paused = False

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                direction = (0, -1)
            elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                direction = (0, 1)
            elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                direction = (-1, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                direction = (1, 0)
            elif event.key == pygame.K_p and not game_over:
                paused = not paused
            elif event.key == pygame.K_r:
                snake, food, direction, score, game_over = reset_game()
                paused = False
            elif event.key == pygame.K_ESCAPE:
                running = False

    if not paused and not game_over:
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0] * CELL,
                    head_y + direction[1] * CELL)

        left, right = 0, WIDTH - CELL
        top, bottom = TOP_BAR, HEIGHT - CELL

        # Wall collision
        if new_head[0] < left or new_head[0] > right or new_head[1] < top or new_head[1] > bottom:
            game_over = True
        # Self collision
        elif new_head in snake:
            game_over = True
        else:
            snake.insert(0, new_head)

            if new_head == food:
                score += 10
                best_score = max(best_score, score)
                food = random_food(snake)
            else:
                snake.pop()

    # Draw
    screen.blit(BACKGROUND, (0, 0))

    # Top bar
    pygame.draw.rect(screen, (8, 24, 31), (0, 0, WIDTH, TOP_BAR))
    pygame.draw.line(screen, (45, 110, 85), (0, TOP_BAR-1), (WIDTH, TOP_BAR-1), 2)

    draw_text(screen, "NEON SNAKE", BIG_FONT, GREEN, (28, 12))
    draw_text(screen, f"SCORE  {score}", FONT, TEXT, (560, 28))
    draw_text(screen, f"BEST  {best_score}", FONT, GOLD, (760, 28))

    # Food glow
    fx, fy = food
    for radius, alpha in [(18, 35), (13, 60)]:
        glow = pygame.Surface((CELL*3, CELL*3), pygame.SRCALPHA)
        pygame.draw.circle(glow, (245, 80, 100, alpha), (CELL*1.5, CELL*1.5), radius)
        screen.blit(glow, (fx - CELL, fy - CELL))
    pygame.draw.circle(screen, RED, (fx + CELL//2, fy + CELL//2), CELL//2 - 3)
    pygame.draw.circle(screen, (255, 155, 170), (fx + CELL//2 - 4, fy + CELL//2 - 5), 4)

    # Snake
    for i, (x, y) in enumerate(snake):
        if i == 0:
            # Rotate head sprite according to direction
            angle = { (1,0): 0, (0,1): -90, (-1,0): 180, (0,-1): 90 }[direction]
            head = pygame.transform.rotate(snake_sprite, angle)
            screen.blit(head, (x - CELL//2, y - CELL//2))
        else:
            rect = pygame.Rect(x+2, y+2, CELL-4, CELL-4)
            pygame.draw.rect(screen, GREEN, rect, border_radius=8)
            pygame.draw.rect(screen, DARK_GREEN, rect, width=2, border_radius=8)
            # scale highlight
            pygame.draw.circle(screen, (100, 230, 130), (x+9, y+8), 2)

    # Bottom hints
    draw_text(screen, "WASD / ARROWS  Move", SMALL_FONT, MUTED, (20, HEIGHT-35))
    draw_text(screen, "P  Pause", SMALL_FONT, MUTED, (390, HEIGHT-35))
    draw_text(screen, "R  Restart", SMALL_FONT, MUTED, (520, HEIGHT-35))
    draw_text(screen, "ESC  Quit", SMALL_FONT, MUTED, (670, HEIGHT-35))

    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 145))
        screen.blit(overlay, (0, 0))
        draw_text(screen, "PAUSED", BIG_FONT, TEXT, (WIDTH//2, HEIGHT//2 - 20), center=True)
        draw_text(screen, "Press P to continue", FONT, MUTED, (WIDTH//2, HEIGHT//2 + 40), center=True)

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        screen.blit(overlay, (0, 0))
        draw_text(screen, "GAME OVER", BIG_FONT, RED, (WIDTH//2, HEIGHT//2 - 65), center=True)
        draw_text(screen, f"Score: {score}   Best: {best_score}", FONT, TEXT, (WIDTH//2, HEIGHT//2 + 5), center=True)
        draw_text(screen, "Press R to play again  •  ESC to quit", FONT, MUTED,
                  (WIDTH//2, HEIGHT//2 + 55), center=True)

    pygame.display.flip()

pygame.quit()
