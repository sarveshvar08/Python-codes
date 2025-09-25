import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game window
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)

# Game variables
gravity = 0.5
bird_movement = 0
bird_x, bird_y = 50, 300
bird_radius = 15

pipe_width = 60
pipe_gap = 150
pipe_velocity = -3

# Font
font = pygame.font.SysFont("Arial", 32)

# Clock
clock = pygame.time.Clock()

# Pipe list
pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# Score
score = 0


def draw_bird(y):
    pygame.draw.circle(win, (255, 255, 0), (bird_x, int(y)), bird_radius)


def create_pipe():
    height = random.randint(100, 400)
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_rect = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT)
    return top_rect, bottom_rect


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx += pipe_velocity
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(win, GREEN, pipe)


def check_collision(pipes, bird_y):
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
        return False
    for pipe in pipes:
        if pipe.colliderect(pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)):
            return False
    return True


# Game loop
running = True
while running:
    win.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -8

        if event.type == SPAWNPIPE:
            pipes.extend(create_pipe())

    # Bird movement
    bird_movement += gravity
    bird_y += bird_movement

    # Draw bird
    draw_bird(bird_y)

    # Pipe movement
    pipes = move_pipes(pipes)
    draw_pipes(pipes)

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.right > 0]

    # Check collisions
    if not check_collision(pipes, bird_y):
        running = False

    # Score
    for pipe in pipes:
        if pipe.centerx == bird_x:
            score += 0.5  # each pipe pair adds 1

    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    win.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

# Game Over
print("Game Over! Final Score:", int(score))
