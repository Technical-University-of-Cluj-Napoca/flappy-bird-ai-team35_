import pygame


class SpriteSheet:
    def __init__(self, filename, cell):
        self.sheet = pygame.image.load(filename).convert()
        w, h = self.sheet.get_size()
        self.w, self.h = w // cell[0], h // cell[1]
        self.cell_width, self.cell_height = cell

    def get_tilecount(self) -> int:
        return self.w * self.h

    def get_tilesize(self) -> tuple[int, int]:
        return (self.cell_width, self.cell_height)

    def image_at_1d(self, idx, cells=(1, 1), colorkey=None) -> pygame.Surface:
        x, y = idx % self.w, idx // self.w
        return self.image_at((x, y), cells, colorkey)

    def image_at(self, pos, cells=(1, 1), colorkey=None) -> pygame.Surface:
        x, y = pos
        cell_x, cell_y = cells
        rect = pygame.Rect(
            (
                x * self.cell_width,
                y * self.cell_height,
                cell_x * self.cell_width,
                cell_y * self.cell_height,
            )
        )
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]
