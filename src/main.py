from sheet import SpriteSheet
from sprite import AnimatedSprite
from utils import Timer, dist
from flappy import Flappy
from pipe import Pipes
from bird_nn import BirdBrain, BrainyBird
from population import Population
from label import NumberLabel
import pickle
import pygame
import random
import time
import os

BG_FILE = "res/bg1.png"
save_file = "scores"


def create_pipes():
    global pipes, width
    pipes = Pipes(width, 2, 60)

def save_scores():
    global hscores, hscores_auto
    with open(save_file, "wb") as f:
        pickle.dump((hscores, hscores_auto), f)

def load_scores():
    global hscores, hscores_auto

    if not os.path.isfile(save_file):
        hscores = []
        hscores_auto = []
        return

    with open(save_file, "rb") as f:
        (hscores, hscores_auto) = pickle.load(f)
        print(hscores, hscores_auto)

def draw_hscores():
    global screen, width, height, hscores, hscores_auto, score_label
    margin = 10
    popup = pygame.Rect(margin, margin, width - 2 * margin, height - 2 * margin)
    pygame.draw.rect(screen, (222, 215, 152), popup)

    score_label.x = margin + 2
    for i, s in enumerate(hscores):
        score_label.y = i * 10 + margin + 2
        score_label.draw(screen, s)

    score_label.x = margin + (width - 2 * margin) / 2
    for i, s in enumerate(hscores_auto):
        score_label.y = i * 10 + margin + 2
        score_label.draw(screen, s)

def update(delta: float):
    global flappy, running, show_scores

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_h:
            show_scores = not show_scores


def physics_update(delta: float):
    global screen, flappy, pipes, height, width, number_label, score, hscores, hscores_auto, show_scores

    keys = pygame.key.get_pressed()
    score += pipes.physics_update(delta)

    if manual:
        flappy.physics_update(delta, keys[pygame.K_SPACE])

        if pipes.collide_flappy(flappy) or flappy.y < 0 or flappy.y > height:
            hscores.append(score)
            hscores.sort(reverse=True)
            hscores = hscores[:10]
            save_scores()
            score = 0
            exit(0)
    else:
        for bb in pop.birds:
            if not bb.alive:
                continue

            bb.physics_update(delta, pipes)

            if pipes.collide_flappy(bb.bird) or bb.bird.y < 0 or bb.bird.y > height:
                bb.die()

        if pop.all_dead():
            create_pipes()
            hscores_auto.append(score)
            hscores_auto.sort(reverse=True)
            hscores_auto = hscores_auto[:10]
            save_scores()
            score = 0
            pop.next_generation()

    if show_scores:
        draw_hscores()
    else:
        bg.draw(screen)

        pipes.draw(screen)

        if manual:
            flappy.draw(screen)
        else:
            for bb in pop.birds:
                if not bb.alive:
                    continue
                bb.draw(screen)

        score_label.x = 2
        score_label.y = 2
        score_label.draw(screen, score)

    pygame.display.flip()


if __name__ == "__main__":
    global width, height, screen, score, running, flappy, bg, pipes, pop, manual, score_label, show_scores
    width = 144
    height = 256

    screen = pygame.display.set_mode((width, height), flags=pygame.SCALED)
    pygame.display.set_caption("Flappy Bird")

    pygame.font.init()
    font = pygame.font.Font(None, 16)

    score_label = NumberLabel("res/numbers.png", colorkey=(255, 255, 255))
    score = 0

    load_scores()

    random.seed(time.time())

    show_scores = False
    manual = False
    if manual:
        flappy = Flappy()
    else:
        pop = Population(4000, 2, mutation_rate=0.9, mutation_strength=0.2)

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
            # game_physics_delta *= 2
            physics_update(game_physics_delta)
            game_physics_delta = 0
