from sheet import SpriteSheet
from drawable import Drawable

class NumberLabel(Drawable):
    def __init__(self, png_font_file: str, colorkey=None):
        super().__init__()
        sheet = SpriteSheet(png_font_file, (6, 7))
        self.numbers = [sheet.image_at((i, 0), colorkey=colorkey) for i in range(10)]

    def draw(self, screen, number):
        for i, c in enumerate(str(number)):
            screen.blit(self.numbers[ord(c) - ord('0')], (self.x + i * 6, self.y))
