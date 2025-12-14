from sprite import AnimatedSprite
from utils import clamp
import pygame


loaded_tiles = None
def new_flappy_sprite():
    global loaded_tiles
    sprite = AnimatedSprite(Flappy.flappy_file, (Flappy.sprite_width, Flappy.sprite_height), -1, 0.1)

    if loaded_tiles is not None:
        sprite.use_loaded(loaded_tiles)

    sprite.new_animation("flap", [(0, 0), (1, 0), (2, 0)])
    sprite.new_animation("fall", [(0, 0)])

    if loaded_tiles is None:
        loaded_tiles = sprite.loaded_tiles

    return sprite

class Flappy:
    flappy_file = "res/flabby.png"
    sprite_width = 17
    sprite_height = 12

    gravity = 700
    jump = 200
    max_vel = 300

    def __init__(self):
        self.sprite = new_flappy_sprite()
        self.sprite.play("fall")
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

    def collision_box(self):
        return pygame.Rect(self.x, self.y, Flappy.sprite_width, Flappy.sprite_height)

    def update(self, delta: float):
        pass

    def physics_update(self, delta: float, jump: bool):
        self.vy += Flappy.gravity * delta

        if jump and self.vy >= -7:
            self.vy = -Flappy.jump
            self.sprite.play("flap", repeat=False)

        if self.vy > 0:
            self.sprite.play("fall")

        self.vy = clamp(self.vy, -Flappy.max_vel, Flappy.max_vel)

        self.sprite.update(delta)

        self.x += self.vx * delta
        self.y += self.vy * delta

    def draw(self, screen):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw(screen)
