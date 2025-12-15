from sheet import SpriteSheet
from sprite import AnimatedSprite
from utils import Timer, dist
from flappy import Flappy
from pipe import Pipes
from bird_nn import BirdBrain, BrainyBird
import pygame
import time

BG_FILE = "res/bg1.png"


def update(delta: float):
    global flappy, running

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False


def physics_update(delta: float):
    global screen, flappy, pipes

    keys = pygame.key.get_pressed()
    pipes.physics_update(delta)
    flappy.physics_update(delta, keys[pygame.K_SPACE])

    if pipes.collide_flappy(flappy):
        exit(0)

    bg.draw(screen)

    pipes.draw(screen)
    flappy.draw(screen)

    pygame.display.flip()


if __name__ == "__main__":
    global width, height, screen, score, running, flappy, bg, pipes
    width = 144
    height = 256

    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED)
    pygame.display.set_caption("Flappy Bird")

    pygame.font.init()
    font = pygame.font.Font(None, 16)

    score = 0

    flappy = Flappy()

    bg = AnimatedSprite(BG_FILE, (width, height))

    pipes = Pipes(width, 2, 50)

    running = True
    t = time.time()

    game_fps = 60
    game_spf = 1 / game_fps
    game_physics_delta = 0
    max_delta = 0
    while running:
        delta = time.time() - t
        t = time.time()

        update(delta)

        game_physics_delta += delta
        if game_physics_delta >= game_spf:
            physics_update(game_physics_delta)
            game_physics_delta = 0
