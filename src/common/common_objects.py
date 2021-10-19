import pygame as pg
from src.surface.base_surface import BaseSurface
from src.surface.surfaces import BackgroundSurface
from src.surface.surfaces import HpBarSurface
from src.surface.surfaces import PotionBarSurface
from src.surface.surfaces import TextSurface
from src.sound.sound import sound
from src.common.config import SCALE
from src.common.config import TILE_WIDTH
from src.common.config import TILE_HEIGHT
from src.common.config import SCREEN_WIDTH
from src.common.config import MAX_HP


class BaseSprite(pg.sprite.Sprite):
    def __init__(self, state=None):
        super().__init__()
        self.state = state
        self.surface: BaseSurface = None
        self.priority = 0

    def set_rotation(self, rotation):
        self.surface.rotate(rotation)

    def get_image(self):
        return self.surface.get_surface()

    def get_rect(self):
        pass

    def update(self, now):
        self.surface.update(now)

    # passing get_image and get_rect alone doesn't work with inheritance
    image = property(fget=lambda self: self.get_image())
    rect = property(fget=lambda self: self.get_rect())


class Text(BaseSprite):
    def __init__(self, position, text="", anchor="center", size=40, font="LemonMilkMediumItalic-d95nl.otf", color=(255, 255, 255)):
        super().__init__()
        self.surface = TextSurface(size=size, font=font, color=color)
        self.surface.set_text(text)
        self.position = position
        self.anchor = anchor

    def set_text(self, text):
        self.surface.set_text(text)

    def get_rect(self):
        return self.surface.get_surface().get_rect(**{self.anchor: self.position})


class Button(BaseSprite):
    def __init__(self, position, text="", anchor="center", function=None, size=40, font="LemonMilkMediumItalic-d95nl.otf", color=(255,255,255)):
        super().__init__()
        self.surface = TextSurface(size=size, font=font, color=color)
        self.surface.set_text(text)
        self.position = position
        self.anchor = anchor
        self.function = function

    def set_text(self, text):
        self.surface.set_text(text)

    def click(self, mouse_pos):
        if self.get_rect().collidepoint(mouse_pos) and self.function is not None:
            sound.play_sound("menu-click.mp3")
            self.function()

    def get_rect(self):
        return self.surface.get_surface().get_rect(**{self.anchor: self.position})


class StaticBlock(BaseSprite):
    def __init__(self, tile_surface, idx, map_width):
        super().__init__()
        self.pos_x = idx % map_width
        self.pos_y = int(idx / map_width)
        self.surface = tile_surface

    def get_rect(self):
        return self.surface.get_surface().get_rect(topleft=(self.pos_x * TILE_WIDTH * SCALE, self.pos_y * TILE_HEIGHT * SCALE))


class PotionBar(BaseSprite):
    def __init__(self, remain=0, anchor="topright", position=(SCREEN_WIDTH - 10, 50)):
        super().__init__()
        self.remain = remain
        self.position = position
        self.anchor = anchor
        self.surface = PotionBarSurface()

    def set_remain(self, remain):
        self.remain = remain
        self.surface.set_remain(remain)

    def get_rect(self):
        return self.surface.get_surface().get_rect(**{self.anchor: self.position})


class HpBar(BaseSprite):
    def __init__(self, hp, anchor="topright", position=(SCREEN_WIDTH - 10, 10)):
        super().__init__()
        self.hp = hp
        self.position = position
        self.anchor = anchor
        self.surface = HpBarSurface()
        self.surface.set_hp(hp)

    def increase_hp(self, amount):
        hp = self.hp + amount
        if hp > MAX_HP:
            hp = MAX_HP
        self.set_hp(hp)

    def decrease_hp(self, amount):
        self.set_hp(self.hp - amount)
        if self.hp <= 0:
            return False
        return True

    def set_hp(self, hp):
        self.hp = hp
        self.surface.set_hp(hp)

    def get_rect(self):
        return self.surface.get_surface().get_rect(**{self.anchor: self.position})


class BackGround(BaseSprite):
    def __init__(self):
        super().__init__()
        self.surface = BackgroundSurface()
        self.offset_x = 0
        self.offset_y = 0

    def update(self, now):
        super().update(now)
        self.offset_x = self.offset_x - 1
        if self.offset_x <= - 64 * SCALE:
            self.offset_x = 0

    def get_rect(self):
        return self.surface.get_surface().get_rect(topleft=(self.offset_x, self.offset_y))
