import pygame as pg
from src.common.map_loader import load_map
from src.surface.surfaces import Terrain
from src.common.common_objects import StaticBlock
from src.common.config import TITLE_WIDTH


class Map:
    def __init__(self, game):
        self.terrain = Terrain()
        self.game = game
        map_name = "title.json"
        layers_data = load_map(map_name)
        self.layers = []
        self.body_shape = []
        for layer in layers_data:
            if layer["name"] in ["Terrain"]:
                group = pg.sprite.Group()
                for idx, tile in enumerate(layer["data"]):
                    if tile != 0:
                        group.add(StaticBlock(self.convert_tile_to_surface(tile), idx, TITLE_WIDTH))
                self.layers.append(group)

    def convert_tile_to_surface(self, tile_id):
        if 1 <= int(tile_id) <= 242:
            return self.terrain.get_tile(tile_id)
        else:
            raise Exception("invalid tile_id")
# class Field(BaseSprite):
#     def __init__(self, game):
#         super().__init__(game)
#         self.surface = FieldSurface()
#
#     def get_rect(self):
#         return self.surface.get_surface().get_rect(topleft=(0, 0))
#
#
# class PressKeyText(BaseSprite):
#     def __init__(self, game):
#         super().__init__(game)
#         self.surface = TextSurface()
#         self.surface.set_text("Press any key to start")
#
#     def get_rect(self):
#         return self.surface.get_surface().get_rect(midtop=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
#
#
# class ControlGuideLeft(BaseSprite):
#     def __init__(self, game):
#         super().__init__(game)
#         self.surface = TextSurface(30)
#         self.surface.set_text("Left controls: Move(W, A, S, D), Switch(Q, E), Shoot(SPACE)")
#
#     def get_rect(self):
#         return self.surface.get_surface().get_rect(topleft=(100, 100))
#
#
# class ControlGuideRight(BaseSprite):
#     def __init__(self, game):
#         super().__init__(game)
#         self.surface = TextSurface(30)
#         self.surface.set_text("Right controls: Move(U, D, L, R), Switch(/, R_SHIFT), Shoot(ENTER)")
#
#     def get_rect(self):
#         return self.surface.get_surface().get_rect(bottomleft=(100, 160))
#
#
# class Score(BaseSprite):
#     def __init__(self, game):
#         super().__init__(game)
#         self.team0 = 0
#         self.team1 = 0
#         self.surface = TextSurface()
#         self.surface.set_text("")
#
#     def update_score(self, team0=None, team1=None):
#         if team0 is not None:
#             self.team0 = team0
#         if team1 is not None:
#             self.team1 = team1
#         self.surface.set_text("Your final score: " + str(self.team0) + " | " + str(self.team1))
#
#     def get_rect(self):
#         return self.surface.get_surface().get_rect(midtop=(SCREEN_WIDTH/2, 100))
