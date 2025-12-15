from sheet import SpriteSheet
from random import randint
from flappy import Flappy
import pygame


class Pipes:
    pipe_file = "res/pipes.png"
    sprite_height = 160
    sprite_width = 26

    scroll_speed = 100

    def __init__(self, width: int, num_pipes: int, gap: int):
        sheet = SpriteSheet(Pipes.pipe_file, (Pipes.sprite_width, Pipes.sprite_height))
        self.up = sheet.image_at((0, 0), colorkey=-1)
        self.down = sheet.image_at((1, 0), colorkey=(255, 255, 255))
        del sheet

        horiz_gap = ((width + Pipes.sprite_width) - Pipes.sprite_width * num_pipes) / num_pipes
        self.pipes_x = [width + i * (Pipes.sprite_width + horiz_gap) for i in range(num_pipes)]
        self.pipes_y = [76] * num_pipes
        self.gap = gap
        self.num = num_pipes
        self.width = width

    def collide_flappy(self, flappy: Flappy):
        (x, up_y), (_, down_y) = self.next_pipes(flappy)

        pipe_up = pygame.Rect(x, up_y, Pipes.sprite_width, Pipes.sprite_height)
        pipe_down = pygame.Rect(x, down_y, Pipes.sprite_width, Pipes.sprite_height)
        flappy_coll = flappy.collision_box()

        if flappy_coll.colliderect(pipe_up) or flappy_coll.colliderect(pipe_down):
            return True

        return False

    def next_pipes(self, flappy: Flappy):
        min_ = 0
        for i in range(self.num):
            if self.pipes_x[i] + Pipes.sprite_width >= flappy.x and self.pipes_x[i] < self.pipes_x[min_]:
                min_ = i

        x = self.pipes_x[min_]
        up_y = self.pipes_y[min_] - Pipes.sprite_height
        down_y = self.pipes_y[min_] + self.gap

        return ((x, up_y), (x, down_y))

    def physics_update(self, delta: float) -> int:
        score = 0
        for i in range(self.num):
            self.pipes_x[i] -= Pipes.scroll_speed * delta
            if self.pipes_x[i] + Pipes.sprite_width < 0:
                self.pipes_x[i] = self.width
                self.pipes_y[i] = randint(56, 140)
                score += 1
        return score

    def draw(self, screen):
        for x, y in zip(self.pipes_x, self.pipes_y):
            screen.blit(self.up, (x, y - Pipes.sprite_height))
            screen.blit(self.down, (x, y + self.gap))
