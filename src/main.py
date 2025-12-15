from sheet import SpriteSheet
from sprite import AnimatedSprite
from utils import Timer, dist
from flappy import Flappy
from pipe import Pipes
from bird_nn import BirdBrain, BrainyBird
from population import Population
from label import NumberLabel
import pygame
import random
import time

BG_FILE = "res/bg1.png"


def create_pipes():
    global pipes, width
    pipes = Pipes(width, 2, 60)

def update(delta: float):
    global flappy, running

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False


def physics_update(delta: float):
    global screen, flappy, pipes, height, width, number_label, score

    keys = pygame.key.get_pressed()
    score += pipes.physics_update(delta)

    if manual:
        flappy.physics_update(delta, keys[pygame.K_SPACE])

        if pipes.collide_flappy(flappy) or flappy.y < 0 or flappy.y > height:
            print("Dead")
            exit(0)
    else:
        for bb in pop.birds:
            if not bb.alive:
                continue

            bb.physics_update(delta, pipes)

            if pipes.collide_flappy(bb.bird) or bb.bird.y < 0 or bb.bird.y > height:
                bb.die()

        if pop.all_dead():
            print("dead")
            create_pipes()
            score = 0
            pop.next_generation()

    bg.draw(screen)

    pipes.draw(screen)

    if manual:
        flappy.draw(screen)
    else:
        for bb in pop.birds:
            if not bb.alive:
                continue
            bb.draw(screen)

    score_label.draw(screen, score)

    pygame.display.flip()


if __name__ == "__main__":
    global width, height, screen, score, running, flappy, bg, pipes, pop, manual, score_label
    width = 144
    height = 256

    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED)
    pygame.display.set_caption("Flappy Bird")

    pygame.font.init()
    font = pygame.font.Font(None, 16)

    score_label = NumberLabel("res/numbers.png", colorkey=(255, 255, 255))
    score_label.x = 2
    score_label.y = 2
    score = 0

    random.seed(time.time())

    manual = False
    if manual:
        flappy = Flappy()
    else:
        pop = Population(3000, 1.5, mutation_rate=0.9, mutation_strength=0.2)

    bg = AnimatedSprite(BG_FILE, (width, height))

    create_pipes()

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
            game_physics_delta *= 2
            physics_update(game_physics_delta)
            game_physics_delta = 0
