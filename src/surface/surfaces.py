import pygame as pg
import os

from src.surface.base_surface import BaseSurface
from src.surface.base_surface import NoAnimation
from src.surface.base_surface import Animation

from src.common.config import SCREEN_WIDTH
from src.common.config import SCREEN_HEIGHT
from src.common.config import TILE_WIDTH
from src.common.config import TILE_HEIGHT
from src.common.config import SCALE
from src.common.config import PLAYER_WIDTH
from src.common.config import PLAYER_HEIGHT
from src.common.config import PLAYER_SCALE
from src.common.config import FRUIT_WIDTH
from src.common.config import FRUIT_HEIGHT
from src.common.config import FRUIT_SCALE
from src.common.config import SLIME_SCALE
from src.common.config import BOX_SCALE
from src.common.config import BOX_WIDTH
from src.common.config import BOX_HEIGHT
from src.common.config import SLIME_WIDTH
from src.common.config import SLIME_HEIGHT
from src.common.config import POTION_SCALE
from src.common.config import POTION_WIDTH
from src.common.config import POTION_HEIGHT
from src.common.config import HEART_WIDTH
from src.common.config import HP_SPACE
from src.common.config import HEART_HEIGHT
from src.common.config import HEART_SCALE

PROJECT_DIR = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
RESOURCE_DIR = os.path.join(PROJECT_DIR, "resources")
_DEFAULT_COLOR_KEY = -1

images = {}


def load_image(name, alpha=False, color_key=None, scale_x=1, scale_y=1):
    if name in images:
        return images[name]

    file_path = os.path.join(RESOURCE_DIR, name)
    try:
        image = pg.image.load(file_path)
    except pg.error:
        print("Cannot load image: ", file_path)
        raise SystemExit(str(pg.compat.geterror()))
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if color_key is not None:
            if color_key == _DEFAULT_COLOR_KEY:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pg.RLEACCEL)

    image = pg.transform.scale(image, (scale_x * image.get_width(), scale_y * image.get_height()))
    images[name] = image
    return image


class TileSurface(BaseSurface):
    def __init__(self, surface):
        super().__init__()
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(surface)
        }


class Terrain:
    def __init__(self):
        self.surface = load_image("assets\\Terrain\\Terrain.png", True, None, SCALE, SCALE)
        self.offset = 1

    def get_tile(self, tile_id):
        x_loc = (tile_id - self.offset) % 22
        y_loc = int((tile_id - self.offset) / 22)
        tile_surface = self.surface.subsurface(pg.Rect(x_loc * SCALE * TILE_WIDTH,
                                                       y_loc * SCALE * TILE_HEIGHT,
                                                       SCALE * TILE_WIDTH,
                                                       SCALE * TILE_HEIGHT))
        return TileSurface(tile_surface)


class AppleSurface(BaseSurface):
    IDLE_STATE = 1

    def __init__(self):
        super().__init__()
        self.image = load_image("assets\\Fruits\\Apple.png", True, None, FRUIT_SCALE, FRUIT_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.get_sub_surface(0)),
            AppleSurface.IDLE_STATE: Animation(
                [self.get_sub_surface(x) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]])
        }

    def get_sub_surface(self, image_id):
        return self.image.subsurface(
            pg.Rect(image_id * FRUIT_SCALE * FRUIT_WIDTH, 0, FRUIT_SCALE * FRUIT_WIDTH, FRUIT_SCALE * FRUIT_HEIGHT))


class BananaSurface(BaseSurface):
    IDLE_STATE = 1

    def __init__(self):
        super().__init__()
        self.image = load_image("assets\\Fruits\\Bananas.png", True, None, FRUIT_SCALE, FRUIT_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.get_sub_surface(0)),
            BananaSurface.IDLE_STATE: Animation(
                [self.get_sub_surface(x) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]])
        }

    def get_sub_surface(self, image_id):
        return self.image.subsurface(
            pg.Rect(image_id * FRUIT_SCALE * FRUIT_WIDTH, 0, FRUIT_SCALE * FRUIT_WIDTH, FRUIT_SCALE * FRUIT_HEIGHT))


class HeartSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        self.image = load_image("assets\\heart.png", True, None, HEART_SCALE, HEART_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.image)
        }


class PlayerSurface(BaseSurface):
    IDLE_STATE = 1
    RUN_STATE = 2
    JUMP_UP_STATE = 3
    FALL_DOWN_STATe = 4
    DOUBLE_JUMP_STATE = 5
    ATTACK_STATE = 6
    HIT = 7
    DEATH = 8
    IMMUNE = 9
    STRONG_ATTACK_STATE = 10

    def __init__(self):
        super().__init__()
        self.idle_run = load_image("assets\\Player_Idle_Run_Stop.png", True, None, PLAYER_SCALE, PLAYER_SCALE)
        self.jump_fall = load_image("assets\\Player_Jump_Fall_SideWall.png", True, None, PLAYER_SCALE, PLAYER_SCALE)
        self.attack = load_image("assets\\PlayerAttack.png", True, None, PLAYER_SCALE, PLAYER_SCALE)
        self.hit_death = load_image("assets\\PlayerHit_Death.png", True, None, PLAYER_SCALE, PLAYER_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.get_sub_surface(0)),
            PlayerSurface.IDLE_STATE: Animation([self.get_sub_surface(x) for x in [0, 1, 2, 3]]),
            PlayerSurface.RUN_STATE: Animation([self.get_sub_surface(x) for x in [4, 5, 6, 7]]),
            PlayerSurface.JUMP_UP_STATE: NoAnimation(self.get_sub_surface(12)),
            PlayerSurface.FALL_DOWN_STATe: NoAnimation(self.get_sub_surface(14)),
            PlayerSurface.DOUBLE_JUMP_STATE: Animation([self.get_sub_surface(x) for x in [16, 17, 18, 19]]),
            PlayerSurface.ATTACK_STATE: Animation([self.get_sub_surface(x) for x in [26, 27]], loops=1),
            PlayerSurface.STRONG_ATTACK_STATE: Animation([self.get_sub_surface(x) for x in [37, 38, 39]], loops=1),
            PlayerSurface.HIT: Animation([self.get_sub_surface(x) for x in [52, 53, 54, 55]], loops=1),
            PlayerSurface.DEATH: Animation(
                [self.get_sub_surface(x) for x in [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77]]),
            PlayerSurface.IMMUNE: Animation([self.get_sub_surface(x) for x in [52, 53, 54, 55]], loops=3),
        }

    def get_sub_surface(self, image_id):
        if 0 <= image_id <= 11:
            pos_x = image_id % 4
            pos_y = int(image_id / 4)
            return self.idle_run.subsurface(pg.Rect(pos_x * PLAYER_SCALE * PLAYER_WIDTH,
                                                    pos_y * PLAYER_SCALE * PLAYER_HEIGHT,
                                                    PLAYER_SCALE * PLAYER_WIDTH,
                                                    PLAYER_SCALE * PLAYER_HEIGHT))
        elif 12 <= image_id <= 23:
            pos_x = (image_id - 12) % 4
            pos_y = int((image_id - 12) / 4)
            return self.jump_fall.subsurface(pg.Rect(pos_x * PLAYER_SCALE * PLAYER_WIDTH,
                                                     pos_y * PLAYER_SCALE * PLAYER_HEIGHT,
                                                     PLAYER_SCALE * PLAYER_WIDTH,
                                                     PLAYER_SCALE * PLAYER_HEIGHT))
        elif 24 <= image_id <= 51:
            pos_x = (image_id - 24) % 4
            pos_y = int((image_id - 24) / 4)
            return self.attack.subsurface(pg.Rect(pos_x * PLAYER_SCALE * PLAYER_WIDTH,
                                                  pos_y * PLAYER_SCALE * PLAYER_HEIGHT,
                                                  PLAYER_SCALE * PLAYER_WIDTH,
                                                  PLAYER_SCALE * PLAYER_HEIGHT))
        elif 52 <= image_id <= 77:
            pos_x = (image_id - 52) % 13
            pos_y = int((image_id - 52) / 13)
            return self.hit_death.subsurface(pg.Rect(pos_x * PLAYER_SCALE * PLAYER_WIDTH,
                                                     pos_y * PLAYER_SCALE * PLAYER_HEIGHT,
                                                     PLAYER_SCALE * PLAYER_WIDTH,
                                                     PLAYER_SCALE * PLAYER_HEIGHT))
        else:
            raise Exception("invalid player image id")


class SlimeSurface(BaseSurface):
    IDLE_STATE = 1
    ATTACK_STATE = 2
    HIT_STATE = 3

    def __init__(self, slime_type=0):
        super().__init__()
        self.image = load_image("assets\\Slime 32x32.png", True, None, SLIME_SCALE, SLIME_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.get_sub_surface(0)),
            SlimeSurface.IDLE_STATE: Animation([self.get_sub_surface(x + 21 * slime_type) for x in [0, 1, 2, 3, 4]]),
            SlimeSurface.ATTACK_STATE: Animation([self.get_sub_surface(x + 21 * slime_type) for x in [5, 6, 7, 8]],
                                                 loops=1),
            SlimeSurface.HIT_STATE: Animation([self.get_sub_surface(x + 21 * slime_type) for x in [9, 10, 11, 12]],
                                              loops=1),
        }

    def get_sub_surface(self, image_id):
        pos_x = image_id % 21
        pos_y = int(image_id / 21)
        return self.image.subsurface(pg.Rect(pos_x * SLIME_SCALE * SLIME_WIDTH,
                                             pos_y * SLIME_SCALE * SLIME_HEIGHT,
                                             SLIME_SCALE * SLIME_WIDTH,
                                             SLIME_SCALE * SLIME_HEIGHT))


class BossSurface(BaseSurface):
    IDLE_STATE = 1
    ATTACK_STATE = 2
    HIT_STATE = 3

    def __init__(self):
        super().__init__()
        self.image = load_image("assets\\Slime 32x32.png", True, None, SLIME_SCALE, SLIME_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.get_sub_surface(0)),
            SlimeSurface.IDLE_STATE: Animation([self.get_sub_surface(x) for x in [105, 106, 107, 108, 109, 110]]),
            SlimeSurface.ATTACK_STATE: Animation([self.get_sub_surface(x) for x in [115, 116, 117, 118]],
                                                 loops=1),
            SlimeSurface.HIT_STATE: Animation([self.get_sub_surface(x) for x in [119, 120, 121, 122]],
                                              loops=1),
        }

    def get_sub_surface(self, image_id):
        pos_x = image_id % 21
        pos_y = int(image_id / 21)
        return self.image.subsurface(pg.Rect(pos_x * SLIME_SCALE * SLIME_WIDTH,
                                             pos_y * SLIME_SCALE * SLIME_HEIGHT,
                                             SLIME_SCALE * SLIME_WIDTH,
                                             SLIME_SCALE * SLIME_HEIGHT))


class BoxSurface(BaseSurface):
    IDLE_STATE = 1
    HIT_STATE = 2
    BREAK_STATE = 3

    def __init__(self):
        super().__init__()
        self.idle = load_image("assets\\Boxes\\Box1\\Idle.png", True, None, BOX_SCALE, BOX_SCALE)
        self.hit = load_image("assets\\Boxes\\Box1\\Hit (28x24).png", True, None, BOX_SCALE, BOX_SCALE)
        self.break_image = load_image("assets\\Boxes\\Box1\\Break.png", True, None, BOX_SCALE, BOX_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.get_sub_surface(0)),
            BoxSurface.IDLE_STATE: NoAnimation(self.get_sub_surface(0)),
            BoxSurface.HIT_STATE: Animation([self.get_sub_surface(x) for x in [1, 2, 3]], loops=1, fps=24),
            BoxSurface.BREAK_STATE: Animation([self.get_sub_surface(x) for x in [4, 5, 6, 7]], loops=1, fps=24),
        }

    def get_sub_surface(self, image_id):
        if image_id == 0:
            return self.idle
        elif 1 <= image_id <= 3:
            pos_x = image_id - 1
            pos_y = 0
            return self.hit.subsurface(pg.Rect(pos_x * BOX_SCALE * BOX_WIDTH,
                                               pos_y * BOX_SCALE * BOX_HEIGHT,
                                               BOX_SCALE * BOX_WIDTH,
                                               BOX_SCALE * BOX_HEIGHT))
        elif 4 <= image_id <= 7:
            pos_x = image_id - 4
            pos_y = 0
            return self.break_image.subsurface(pg.Rect(pos_x * BOX_SCALE * BOX_WIDTH,
                                                       pos_y * BOX_SCALE * BOX_HEIGHT,
                                                       BOX_SCALE * BOX_WIDTH,
                                                       BOX_SCALE * BOX_HEIGHT))


class PotionSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        self.image = load_image("assets\\potion.png", True, None, POTION_SCALE, POTION_SCALE)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(self.image)
        }


class TextSurface(BaseSurface):
    def __init__(self, size=60, font=None, color=(255, 255, 255)):
        super().__init__()
        font_path = os.path.join(RESOURCE_DIR, "font", font) if font is not None else None
        self.font = pg.font.Font(font_path, size)
        self.surface = None
        self.color = color

    def set_text(self, text: str):
        self.surface = self.font.render(text, True, self.color)

    def update(self, now):
        pass

    def get_surface(self) -> pg.Surface:
        return self.surface


class HpBarSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        self.hp = 0
        self.heart = load_image("assets\\heart.png", True, None, HEART_SCALE, HEART_SCALE)
        self.surface = self.draw_hp_bar()

    def draw_hp_bar(self):
        if self.hp <= 0:
            return pg.Surface((0, 0))

        surface = pg.Surface(((HEART_WIDTH * HEART_SCALE + HP_SPACE) * self.hp - HP_SPACE, HEART_HEIGHT * HEART_SCALE), pg.SRCALPHA)
        for i in range(self.hp):
            surface.blit(self.heart, ((HEART_WIDTH * HEART_SCALE + HP_SPACE) * i, 0))
        return surface

    def set_hp(self, hp):
        self.hp = hp
        self.surface = self.draw_hp_bar()

    def update(self, now):
        pass

    def get_surface(self) -> pg.Surface:
        return self.surface


class PotionBarSurface(BaseSurface):
    def __init__(self, div=100):
        self.div = div
        self.remain = 0
        self.potion = load_image("assets\\potion.png", True, None, POTION_SCALE, POTION_SCALE)
        self.surface = self.draw_potion_bar()
        self.font = pg.font.Font(None, 40)

    def draw_potion_bar(self):
        if int(self.remain/self.div) <= 0:
            return pg.Surface((0, 0))

        text_surface = self.font.render(str(int(self.remain/self.div)), True, (255,255,255))
        surface_height = max(POTION_HEIGHT * POTION_SCALE, text_surface.get_height())
        surface = pg.Surface((POTION_WIDTH * POTION_SCALE + HP_SPACE + text_surface.get_width(), surface_height), pg.SRCALPHA)
        surface.blit(self.potion, (0, 0))
        surface.blit(text_surface, (POTION_WIDTH * POTION_SCALE + HP_SPACE, (surface_height - text_surface.get_height())/2))
        return surface

    def set_remain(self, remain):
        old_remain = self.remain
        self.remain = remain
        if int(old_remain/self.div) != int(remain/self.div):
            self.surface = self.draw_potion_bar()

    def update(self, now):
        pass

    def get_surface(self) -> pg.Surface:
        return self.surface


class BackgroundSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        image = load_image("assets\\Background\\Blue.png")
        surface = pg.Surface((SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))
        for i in range(int(SCREEN_WIDTH / (2 * TILE_WIDTH * SCALE)) + 3):
            for j in range(int(SCREEN_HEIGHT / (2 * TILE_HEIGHT * SCALE)) + 3):
                surface.blit(image, (i * 2 * TILE_WIDTH * SCALE, j * 2 * TILE_HEIGHT * SCALE))
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(surface)
        }

# class BallSurface(BaseSurface):
#     def __init__(self):
#         super().__init__()
#         global _BALL_IMAGE
#         if _BALL_IMAGE is None:
#             image_name = "ball.png"
#             _BALL_IMAGE = load_image(image_name, alpha=True)
#         image = _BALL_IMAGE
#         image = pg.transform.scale(image, (2*BALL_RADIUS, 2*BALL_RADIUS))
#         self.radius = BALL_RADIUS
#         self.images = {
#             BaseSurface.DEFAULT_STATE: NoAnimation(image)
#         }
#
#

#
#
# class LineSurface(BaseSurface):
#     def __init__(self, width, length):
#         super().__init__()
#         rect = pg.Surface((length, width), pg.SRCALPHA)
#         rect.fill((0, 0, 0, 0))
#         self.images = {
#             BaseSurface.DEFAULT_STATE: NoAnimation(rect)
#         }
#
#
#
#
# class GoalSurface(BaseSurface):
#     def __init__(self):
#         super().__init__()
#         rect_surface = pg.Surface((GOAL_WIDTH, GOAL_HEIGHT), pg.SRCALPHA)
#         pg.draw.rect(rect_surface, (0, 90, 90, 0), pg.rect.Rect(0, 0, GOAL_WIDTH, GOAL_HEIGHT))
#         self.images = {
#             BaseSurface.DEFAULT_STATE: NoAnimation(rect_surface)
#         }
#
#
# class TextSurface(BaseSurface):
#     def __init__(self, size=60):
#         super().__init__()
#         self.font = pg.font.Font(None, size)
#         self.surface = None
#
#     def set_text(self, text:str):
#         self.surface = self.font.render(text, True, (255, 255, 255))
#
#     def update(self, now):
#         pass
#
#     def get_surface(self) -> pg.Surface:
#         return self.surface
