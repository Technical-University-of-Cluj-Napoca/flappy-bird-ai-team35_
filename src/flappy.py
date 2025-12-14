from sprite import AnimatedSprite
from utils import clamp
import pygame

FLAPPY_FILE = "res/flabby.png"

class Flappy:
    gravity = 400
    jump = 120
    max_vel = 500

    def __init__(self):
        self.sprite = AnimatedSprite(FLAPPY_FILE, (17, 12), -1, 0.1)
        self.sprite.new_animation("flap", [(0, 0), (1, 0), (2, 0)])
        self.sprite.new_animation("fall", [(0, 0)])
        self.sprite.play("fall")
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

    def update(self, delta: float):
        pass

    def physics_update(self, delta: float):
        self.vy += Flappy.gravity * delta

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
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
