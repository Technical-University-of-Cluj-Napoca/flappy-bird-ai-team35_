from sheet import SpriteSheet
from drawable import Drawable
import pygame


class AnimatedSprite(Drawable):
    def __init__(
        self,
        sheet_file: str,
        tilesize: tuple[int, int],
        colorkey=None,
        frame_speed: float = 0.5,
        reset_frame: tuple[int, int] = (0, 0),
    ):
        super().__init__()
        self.sheet = SpriteSheet(sheet_file, tilesize)
        self.colorkey = colorkey
        self.loaded_tiles = [None] * self.sheet.get_tilecount()
        self.anims = dict()
        self.paused = False
        self.new_animation("RESET", [reset_frame])
        self.anim = None
        self.play("RESET")
        self.frame = 0
        self.delta_acc = 0
        self.fs = frame_speed

    def get_size(self) -> tuple[int, int]:
        return self.sheet.get_tilesize()

    def get_tile(self, idx: int) -> pygame.Surface:
        if idx < 0 or idx >= self.sheet.get_tilecount():
            raise ValueError(f"Tile index {idx} is out of bounds")

        if not self.loaded_tiles[idx]:
            self.loaded_tiles[idx] = self.sheet.image_at_1d(idx, colorkey=self.colorkey)

        return self.loaded_tiles[idx]

    def new_animation(self, name: str, frames: list[tuple[int, int]]):
        self.anims[name] = []
        for frame_coord in frames:
            x, y = frame_coord
            idx = x + y * self.sheet.w
            self.anims[name].append(self.get_tile(idx))

    def play(self, name: str, repeat: bool = True):
        if self.anim == name:
            return

        self.frame = 0
        self.anim = name
        self.paused = False
        self.repeat = repeat

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def is_paused(self):
        return self.paused

    def update(self, delta: float):
        if self.paused:
            return

        self.delta_acc += delta

        if self.delta_acc >= self.fs:
            self.delta_acc -= self.fs
            self.frame += 1
            if self.frame >= len(self.anims[self.anim]):
                if self.repeat:
                    self.frame = 0
                else:
                    self.frame -= 1
                    self.pause()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.anims[self.anim][self.frame], (self.x, self.y))
