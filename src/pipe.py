from sheet import SpriteSheet
from random import randint
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

    def physics_update(self, delta: float):
        for i in range(self.num):
            self.pipes_x[i] -= Pipes.scroll_speed * delta
            if self.pipes_x[i] + Pipes.sprite_width < 0:
                self.pipes_x[i] = self.width
                self.pipes_y[i] = randint(56, 140)

    def draw(self, screen):
        for x, y in zip(self.pipes_x, self.pipes_y):
            screen.blit(self.up, (x, y - Pipes.sprite_height))
            screen.blit(self.down, (x, y + self.gap))
