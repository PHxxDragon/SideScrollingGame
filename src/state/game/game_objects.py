import random

import pygame as pg
import pymunk

from src.surface.surfaces import PlayerSurface
from src.surface.surfaces import AppleSurface
from src.surface.surfaces import HeartSurface
from src.surface.surfaces import SlimeSurface
from src.surface.surfaces import BoxSurface
from src.surface.surfaces import BossSurface
from src.surface.surfaces import PotionSurface
from src.surface.surfaces import Terrain
from src.common.map_loader import load_map
from src.sound.sound import sound
from src.common.config import SCREEN_WIDTH
from src.common.config import SCREEN_HEIGHT
from src.common.config import TILE_WIDTH
from src.common.config import TILE_HEIGHT
from src.common.config import UP_BLOCK
from src.common.config import LEFT_BLOCK
from src.common.config import RIGHT_BLOCK
from src.common.config import DOWN_BLOCK
from src.common.config import MAP_WIDTH
from src.common.config import MAP_HEIGHT
from src.common.config import SCALE
from src.common.config import PLAYER_BOX_WIDTH
from src.common.config import PLAYER_BOX_HEIGHT
from src.common.config import FRUIT_SCALE
from src.common.config import SLIME_SCALE
from src.common.config import FRUIT_BOX_WIDTH
from src.common.config import FRUIT_BOX_HEIGHT
from src.common.config import SLIME_BOX_WIDTH
from src.common.config import SLIME_BOX_HEIGHT
from src.common.config import BOSS_BOX_WIDTH
from src.common.config import BOSS_BOX_HEIGHT
from src.common.config import FRUIT_WIDTH
from src.common.config import FRUIT_HEIGHT
from src.common.config import SLIME_WIDTH
from src.common.config import SLIME_HEIGHT
from src.common.config import PLAYER_SCALE
from src.common.config import BOX_WIDTH
from src.common.config import BOX_HEIGHT
from src.common.config import HEART_WIDTH
from src.common.config import HEART_HEIGHT
from src.common.config import POTION_WIDTH
from src.common.config import POTION_HEIGHT
from src.common.config import POTION_BOX_WIDTH
from src.common.config import POTION_BOX_HEIGHT
from src.common.config import POTION_SCALE
from src.common.config import BOX_SCALE
from src.common.config import BOX_BOX_WIDTH
from src.common.config import BOX_BOX_HEIGHT
from src.common.config import PLAYER_COLLISION_TYPE
from src.common.config import UP_SEGMENT_COLLISION_TYPE
from src.common.config import WALL_COLLISION_TYPE
from src.common.config import PLAYER_ATTACK_RECT_WIDTH
from src.common.config import PLAYER_ATTACK_RECT_HEIGHT
from src.common.config import FRUIT_COLLISION_TYPE
from src.common.common_objects import BaseSprite
from src.common.common_objects import StaticBlock


class Map:
    def __init__(self, game):
        self.terrain = Terrain()
        self.game = game
        map_name = "map1.json"
        layers_data = load_map(map_name)
        self.layers = []
        self.body_shape = []
        self.target_groups = []
        for layer in layers_data:
            if layer["name"] in ["Terrain"]:
                group = pg.sprite.Group()
                for idx, tile in enumerate(layer["data"]):
                    if tile != 0:
                        group.add(StaticBlock(self.convert_tile_to_surface(tile), idx, MAP_WIDTH))
                self.layers.append(group)

                up, down, left, right = self.get_all_segments(layer["data"])
                for (x_min, y), (x_max, _) in up:
                    body = pymunk.Body(body_type=pymunk.Body.STATIC)
                    shape = pymunk.Segment(body=body, a=(x_min * TILE_WIDTH * SCALE, y * TILE_WIDTH * SCALE), b=((x_max + 1) * TILE_WIDTH * SCALE, y * TILE_WIDTH * SCALE), radius=1)
                    shape.elasticity = 0.0
                    shape.collision_type = UP_SEGMENT_COLLISION_TYPE
                    game.space.add(body, shape)
                for (x_min, y), (x_max, _) in down:
                    body = pymunk.Body(body_type=pymunk.Body.STATIC)
                    shape = pymunk.Segment(body=body, a=(x_min * TILE_WIDTH * SCALE, (y + 1) * TILE_WIDTH * SCALE), b=((x_max + 1) * TILE_WIDTH * SCALE, (y + 1) * TILE_WIDTH * SCALE), radius=1)
                    shape.elasticity = 0.0
                    shape.collision_type = WALL_COLLISION_TYPE
                    game.space.add(body, shape)
                for (x, y_min), (x, y_max) in left:
                    body = pymunk.Body(body_type=pymunk.Body.STATIC)
                    shape = pymunk.Segment(body=body, a=(x * TILE_WIDTH * SCALE, y_min * TILE_WIDTH * SCALE), b=(x * TILE_WIDTH * SCALE, (y_max + 1) * TILE_WIDTH * SCALE), radius = 1)
                    shape.elasticity = 0.0
                    shape.collision_type = WALL_COLLISION_TYPE
                    game.space.add(body, shape)
                for (x, y_min), (x, y_max) in right:
                    body = pymunk.Body(body_type=pymunk.Body.STATIC)
                    shape = pymunk.Segment(body=body, a=((x + 1) * TILE_WIDTH * SCALE, y_min * TILE_WIDTH * SCALE),
                                                b=((x + 1) * TILE_WIDTH * SCALE, (y_max + 1) * TILE_WIDTH * SCALE), radius=1)
                    shape.elasticity = 0.0
                    game.space.add(body, shape)
            if layer["name"] in ["Fruits"]:
                group = pg.sprite.Group()
                for obj in layer["objects"]:
                    if obj["gid"] == 705:
                        group.add(Apple(game, (SCALE * (obj["x"] + FRUIT_WIDTH/2), SCALE * (obj["y"] - FRUIT_HEIGHT/2))))
                self.layers.append(group)
            if layer["name"] in ["Slimes"]:
                group = pg.sprite.Group()
                for obj in layer["objects"]:
                    if obj["gid"] == 739:
                        group.add(BlueSlime(game, (SCALE * (obj["x"] + SLIME_WIDTH/2), SCALE * (obj["y"] - SLIME_HEIGHT/2))))
                    if obj["gid"] == 844:
                        group.add(BossSlime(game, (SCALE * (obj["x"] + SLIME_WIDTH/2), SCALE * (obj["y"] - SLIME_HEIGHT/2))))
                self.layers.append(group)
                self.target_groups.append(group)
            if layer["name"] in ["Boxes"]:
                group = pg.sprite.Group()
                for obj in layer["objects"]:
                    if obj["gid"] == 949:
                        item = None
                        if "properties" in obj:
                            for prop in obj["properties"]:
                                if prop["name"] == "item":
                                    item = prop["value"]
                        group.add(Box(game, (SCALE * (obj["x"] + BOX_WIDTH/2), SCALE * (obj["y"] - BOX_HEIGHT/2)), item=item))
                self.layers.append(group)
                self.target_groups.append(group)
            if layer["name"] in ["Items"]:
                group = pg.sprite.Group()
                for obj in layer["objects"]:
                    if obj["gid"] == 950:
                        group.add(HeartItem(game, (SCALE * (obj["x"] + HEART_WIDTH/2), SCALE * (obj["y"] - HEART_HEIGHT/2))))
                    elif obj["gid"] == 951:
                        group.add(PotionItem(game, (SCALE * (obj["x"] + POTION_WIDTH/2), SCALE * (obj["y"] - POTION_HEIGHT/2))))
                self.layers.append(group)


    @staticmethod
    def convert_arr_to_max(idx, width):
        return idx % width, int(idx / width)

    @staticmethod
    def convert_max_to_arr(x, y, width):
        return x + y * width

    def get_all_segments(self, layer):
        up_segments = []
        marked = [False] * len(layer)
        for idx, tile in enumerate(layer):
            if marked[idx] is False and tile in UP_BLOCK:
                marked[idx] = True
                min_x, y = self.convert_arr_to_max(idx, MAP_WIDTH)
                max_x = min_x
                cur_x = min_x
                while True:
                    cur_x = cur_x + 1
                    if cur_x >= MAP_WIDTH:
                        break
                    cur_idx = self.convert_max_to_arr(cur_x, y, MAP_WIDTH)
                    if layer[cur_idx] in UP_BLOCK:
                        marked[cur_idx] = True
                        max_x = cur_x
                up_segments.append(((min_x, y), (max_x, y)))
        left_segments = []
        marked = [False] * len(layer)
        for idx, tile in enumerate(layer):
            if marked[idx] is False and tile in LEFT_BLOCK:
                marked[idx] = True
                x, min_y = self.convert_arr_to_max(idx, MAP_WIDTH)
                max_y = min_y
                cur_y = min_y
                while True:
                    cur_y = cur_y + 1
                    if cur_y >= MAP_HEIGHT:
                        break
                    cur_idx = self.convert_max_to_arr(x, cur_y, MAP_WIDTH)
                    if layer[cur_idx] in LEFT_BLOCK:
                        marked[cur_idx] = True
                        max_y = cur_y
                left_segments.append(((x, min_y), (x, max_y)))
        right_segments = []
        marked = [False] * len(layer)
        for idx, tile in enumerate(layer):
            if marked[idx] is False and tile in RIGHT_BLOCK:
                marked[idx] = True
                x, min_y = self.convert_arr_to_max(idx, MAP_WIDTH)
                max_y = min_y
                cur_y = min_y
                while True:
                    cur_y = cur_y + 1
                    if cur_y >= MAP_HEIGHT:
                        break
                    cur_idx = self.convert_max_to_arr(x, cur_y, MAP_WIDTH)
                    if layer[cur_idx] in RIGHT_BLOCK:
                        marked[cur_idx] = True
                        max_y = cur_y
                right_segments.append(((x, min_y), (x, max_y)))
        down_segments = []
        marked = [False] * len(layer)
        for idx, tile in enumerate(layer):
            if marked[idx] is False and tile in DOWN_BLOCK:
                marked[idx] = True
                min_x, y = self.convert_arr_to_max(idx, MAP_WIDTH)
                max_x = min_x
                cur_x = min_x
                while True:
                    cur_x = cur_x + 1
                    if cur_x >= MAP_WIDTH:
                        break
                    cur_idx = self.convert_max_to_arr(cur_x, y, MAP_WIDTH)
                    if layer[cur_idx] in DOWN_BLOCK:
                        marked[cur_idx] = True
                        max_x = cur_x
                down_segments.append(((min_x, y), (max_x, y)))
        return up_segments, down_segments, left_segments, right_segments

    def convert_tile_to_surface(self, tile_id):
        if 1 <= int(tile_id) <= 242:
            return self.terrain.get_tile(tile_id)
        else:
            raise Exception("invalid tile_id")


class ItemSpawner:
    def __init__(self, game):
        self.game = game
        self.items = pg.sprite.Group()

    def spawn_item(self, item_id, position):
        if item_id == 950:
            self.items.add(HeartItem(self.game, position))
        elif item_id == 951:
            self.items.add(PotionItem(self.game, position))


class BasePhysicsSprite(BaseSprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.body: pymunk.Body = None
        self.shape: pymunk.Shape = None

    def get_rect(self):
        return self.surface.get_surface().get_rect(center=self.body.position)


class Fruit(BasePhysicsSprite):
    ID = 10000

    def __init__(self, game, position, box_width=FRUIT_BOX_WIDTH, box_height=FRUIT_BOX_HEIGHT, scale=FRUIT_SCALE):
        super().__init__(game)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        self.shape = pymunk.Poly.create_box(body=self.body, size=(box_width * scale, box_height * scale))
        game.space.add(self.body, self.shape)
        self.shape.collision_type = Fruit.ID
        self.shape.sensor = True
        self.collision_handler = game.space.add_collision_handler(PLAYER_COLLISION_TYPE, Fruit.ID)
        self.collision_handler.begin = self.handler
        Fruit.ID = Fruit.ID + 1

    def handler(self, space, arbiter, data):
        self.game.player.eat()
        self.game.space.remove(self.body, self.shape)
        sound.play_sound("fruit.wav")
        self.kill()
        return False

    def get_rect(self):
        return self.surface.get_surface().get_rect(center=self.body.position)


class PotionItem(Fruit):
    def __init__(self, game, position):
        super().__init__(game, position, POTION_BOX_WIDTH, POTION_BOX_HEIGHT, POTION_SCALE)
        self.surface = PotionSurface()

    def handler(self, space, arbiter, data):
        self.game.player.power_up_func()
        self.game.space.remove(self.body, self.shape)
        sound.play_sound("power-up.mp3")
        self.kill()
        return False


class HeartItem(Fruit):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.surface = HeartSurface()

    def handler(self, space, arbiter, data):
        self.game.hp_bar.increase_hp(1)
        self.game.space.remove(self.body, self.shape)
        sound.play_sound("heal.mp3")
        self.kill()
        return False


class Box(BasePhysicsSprite):
    ID = 30000

    def __init__(self, game, position, hp=2, item=None):
        super().__init__(game)
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = position
        self.shape = pymunk.Poly.create_box(body=self.body,
                                            size=(BOX_BOX_WIDTH * BOX_SCALE, BOX_BOX_HEIGHT * BOX_SCALE))
        game.space.add(self.body, self.shape)
        self.shape.collision_type = UP_SEGMENT_COLLISION_TYPE
        self.shape.elasticity = 0
        self.shape.mass = 2
        self.state = None
        self.hp = hp
        self.surface = BoxSurface()
        self.set_state(BoxSurface.IDLE_STATE)
        self.item = item
        Box.ID = Box.ID + 1

    def get_hit(self, damage=1):
        def callback():
            self.hp = self.hp - damage
            if self.hp <= 0:
                def callback2():
                    self.game.space.remove(self.body, self.shape)
                    if self.item is not None:
                        self.game.item_spawner.spawn_item(self.item, self.body.position)
                    self.kill()
                sound.play_sound("break.mp3.flac")
                self.set_state(BoxSurface.BREAK_STATE, callback2)
            else:
                self.set_state(BoxSurface.IDLE_STATE)

        sound.play_sound("hit.mp3.flac")
        self.set_state(BoxSurface.HIT_STATE, callback)

    def set_state(self, state, callback=None):
        self.state = state
        self.surface.set_state(state, callback)

    def get_rect(self):
        return self.surface.get_surface().get_rect(center=self.body.position)


class Slime(BasePhysicsSprite):
    ID = 20000

    def __init__(self, game, position, hp=2, box_width=SLIME_BOX_WIDTH, box_height=SLIME_BOX_HEIGHT, scale=SLIME_SCALE):
        super().__init__(game)
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = position
        self.shape = pymunk.Poly.create_box(body=self.body,
                                            size=(box_width * scale, box_height * scale))
        game.space.add(self.body, self.shape)
        self.shape.collision_type = Slime.ID
        self.shape.elasticity = 0
        self.shape.mass = 2
        self.collision_handler = game.space.add_collision_handler(PLAYER_COLLISION_TYPE, Slime.ID)
        self.collision_handler.begin = self.handler
        self.collision_handler.data["slime"] = self
        self.slime_collision = game.space.add_collision_handler(Slime.ID, Slime.ID)
        self.slime_collision.begin = self.slime_begin_handler
        self.state = None
        self.hp = hp

    @staticmethod
    def slime_begin_handler(space, arbiter, data):
        return False

    def handler(self, space, arbiter, data):
        collide_vector = self.game.player.body.position - data["slime"].body.position
        collide_vector = collide_vector / collide_vector.length
        self.game.player.get_hit(collide_vector)
        return False

    def get_hit(self, damage=1):
        if self.state in [SlimeSurface.HIT_STATE]:
            return

        sound.play_sound("slime-hit.mp3")

        def callback():
            self.hp = self.hp - damage
            if self.hp <= 0:
                self.game.space.remove(self.body, self.shape)
                self.kill()
            self.set_state(SlimeSurface.IDLE_STATE)

        self.set_state(SlimeSurface.HIT_STATE, callback)

    def set_state(self, state, callback=None):
        self.state = state
        self.surface.set_state(state, callback)

    def get_rect(self):
        return self.surface.get_surface().get_rect(center=self.body.position)


class BossSlime(Slime):
    def __init__(self, game, position):
        super().__init__(game, position, hp=30, box_width=BOSS_BOX_WIDTH, box_height=BOSS_BOX_HEIGHT)
        self.surface = BossSurface()
        self.set_state(BossSurface.IDLE_STATE)
        self.face_right = False
        self.ai = BossSlimeAI(game, self)
        self.is_jump = False
        self.body_position_y = self.body.position.y
        self.jump_frames_tolerance = 3
        self.lost_hp = 0
        self.spawn_items = [951, 950, 951, 951, 950, 951]

    def get_hit(self, damage=1):
        super().get_hit(damage)
        self.lost_hp = self.lost_hp + damage
        if self.lost_hp >= 5:
            self.lost_hp = self.lost_hp - 5
            self.game.item_spawner.spawn_item(self.spawn_items[-1], self.body.position)
            self.spawn_items.pop()

    def move_left(self):
        self.face_right = False
        self.body.velocity = (-15, self.body.velocity.y)
        self.surface.set_flip(True)

    def move_right(self):
        self.face_right = True
        self.body.velocity = (15, self.body.velocity.y)
        self.surface.set_flip(False)

    def stop_moving(self):
        self.body.velocity = (0, self.body.velocity.y)

    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.body.velocity = (self.body.velocity.x, -30)

    def update(self, now):
        super().update(now)
        self.jump_frames_tolerance = self.jump_frames_tolerance - 1
        if self.jump_frames_tolerance <= 0:
            self.jump_frames_tolerance = 3
            current_position_y = self.body.position.y
            if abs(current_position_y - self.body_position_y) < 0.1:
                self.is_jump = False
            self.body_position_y = current_position_y
        self.ai.update(now)


class BossSlimeAI:
    def __init__(self, game, slime):
        self.game = game
        self.slime = slime
        self.jump_duration = 50
        self.original_x = self.slime.body.position.x
        self.move_range = 300
        self.turn_duration = 50

    def update(self, now):
        self.jump_duration = self.jump_duration - 1
        self.turn_duration = self.turn_duration - 1
        if self.jump_duration <= 0:
            self.jump_duration = random.randint(50, 150)
            self.slime.jump()

        if self.turn_duration <= 0:
            self.turn_duration = random.randint(50, 110)
            if self.slime.face_right:
                self.slime.move_left()
            else:
                self.slime.move_right()

            if abs(self.game.player.body.position.x - self.original_x) < 300:
                if self.slime.body.position.x > self.game.player.body.position.x:
                    self.slime.move_left()
                else:
                    self.slime.move_right()
        else:
            if self.slime.face_right:
                self.slime.move_right()
            else:
                self.slime.move_left()

        if (self.slime.body.position.x - self.original_x) > self.move_range:
            self.slime.move_left()
        elif (self.slime.body.position.x - self.original_x) < -self.move_range:
            self.slime.move_right()


class BlueSlime(Slime):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.surface = SlimeSurface()
        self.set_state(SlimeSurface.IDLE_STATE)
        self.face_right = False
        self.ai = BlueSlimeAI(game, self)

    def move_left(self):
        self.face_right = False
        self.body.velocity = (-15, self.body.velocity.y)
        self.surface.set_flip(True)

    def move_right(self):
        self.face_right = True
        self.body.velocity = (15, self.body.velocity.y)
        self.surface.set_flip(False)

    def stop_moving(self):
        self.body.velocity = (0, self.body.velocity.y)

    def update(self, now):
        super().update(now)
        self.ai.update(now)


class BlueSlimeAI:
    def __init__(self, game, slime):
        self.game = game
        self.slime = slime
        self.turn_duration = 2
        self.last_x_position = self.slime.body.position[0]

    def update(self, now):
        self.turn_duration = self.turn_duration - 1
        if self.slime.state in [SlimeSurface.HIT_STATE]:
            self.slime.stop_moving()
            return

        if self.turn_duration > 0:
            if self.slime.face_right:
                self.slime.move_right()
            else:
                self.slime.move_left()
        else:
            self.turn_duration = 2
            current_x_position = self.slime.body.position[0]
            if abs(self.last_x_position - current_x_position) < 0.1:
                if self.slime.face_right:
                    self.slime.move_left()
                else:
                    self.slime.move_right()
            self.last_x_position = current_x_position


class Apple(Fruit):
    def __init__(self, game, position):
        super().__init__(game, position)
        self.surface = AppleSurface()
        self.surface.set_state(AppleSurface.IDLE_STATE)


class Player(BasePhysicsSprite):
    def __init__(self, game):
        super().__init__(game)
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = (870, 300)
        self.shape = pymunk.Poly.create_box(body=self.body, size=(PLAYER_BOX_WIDTH * PLAYER_SCALE, PLAYER_BOX_HEIGHT * PLAYER_SCALE))
        self.shape.elasticity = 0.0
        self.shape.collision_type = PLAYER_COLLISION_TYPE
        self.shape.mass = 1
        game.space.add(self.body, self.shape)
        self.surface = PlayerSurface()
        self.set_state(PlayerSurface.IDLE_STATE)
        self.score = 0
        self.collision_handler = game.space.add_collision_handler(PLAYER_COLLISION_TYPE, UP_SEGMENT_COLLISION_TYPE)
        self.collision_handler.begin = self.handler
        self.collision_handler.separate = self.separate
        self.targets = pg.sprite.Group()
        self.face_right = True
        self.on_ground = 0
        self.double_jumped = False
        self.power_up = False
        self.power_up_duration = 0

    def power_up_func(self, duration=1000):
        self.power_up = True
        self.power_up_duration = duration

    def handler(self, space, arbiter, data):
        self.reach_ground()
        return True

    def separate(self, space, arbiter, data):
        self.leave_ground()
        return True

    def eat(self):
        self.score += 1
        self.game.score.set_text("score: " + str(self.score))

    def attack(self):
        if self.state in [PlayerSurface.HIT]:
            return

        self.targets = self.game.target.copy()
        to_be_removed = []
        for sprite in self.targets.sprites():
            if (sprite.body.position - self.body.position).length > 200:
                to_be_removed.append(sprite)
        self.targets.remove(*to_be_removed)

        def callback():
            self.set_state(PlayerSurface.IDLE_STATE)

        if self.power_up:
            sound.play_sound("strong-cut.wav")
            self.set_state(PlayerSurface.STRONG_ATTACK_STATE, callback)
        else:
            sound.play_sound("cut.mp3")
            self.set_state(PlayerSurface.ATTACK_STATE, callback)

    def update(self, now):
        super().update(now)

        if self.state in [PlayerSurface.ATTACK_STATE, PlayerSurface.STRONG_ATTACK_STATE]:
            if self.face_right:
                topright = self.body.position[0] + PLAYER_BOX_WIDTH / 2, self.body.position[1] - PLAYER_BOX_HEIGHT / 2
                attack_rect = pg.Rect(topright[0], topright[1] - 3, PLAYER_ATTACK_RECT_WIDTH * PLAYER_SCALE, PLAYER_ATTACK_RECT_HEIGHT * PLAYER_SCALE)
            else:
                topleft = self.body.position[0] - PLAYER_BOX_WIDTH / 2, self.body.position[1] - PLAYER_BOX_HEIGHT / 2
                attack_rect = pg.Rect(topleft[0] - PLAYER_ATTACK_RECT_WIDTH * PLAYER_SCALE, topleft[1] - 3, PLAYER_ATTACK_RECT_WIDTH * PLAYER_SCALE,
                                      PLAYER_ATTACK_RECT_HEIGHT * PLAYER_SCALE)
            to_be_removed = []
            for sprite in self.targets.sprites():
                bb = sprite.shape.bb
                enemy_rect = pg.Rect(bb.left, bb.top, bb.right - bb.left, bb.bottom - bb.top)
                if attack_rect.colliderect(enemy_rect):
                    sprite.get_hit(2 if self.power_up else 1)
                    to_be_removed.append(sprite)
            self.targets.remove(*to_be_removed)

        if self.power_up:
            self.power_up_duration = self.power_up_duration - 1
            if self.power_up_duration <= 0:
                self.power_up_duration = 0
                self.power_up = False

    def get_hit(self, collide_vector=None):
        if self.state in [PlayerSurface.HIT, PlayerSurface.IMMUNE]:
            return

        sound.play_sound("player-hit.mp3")

        if not self.game.hp_bar.decrease_hp(1):
            self.game.game_over()

        def callback1():
            self.set_state(PlayerSurface.IDLE_STATE)

        def callback():
            self.set_state(PlayerSurface.IMMUNE, callback1)

        self.set_state(PlayerSurface.HIT, callback)
        if collide_vector is not None:
            velocity_x = -1 if collide_vector[0] < 0 else 1
            self.body.velocity = velocity_x * 20, self.body.velocity[1]

    def set_state(self, state, callback=None):
        self.state = state
        self.surface.set_state(state, callback)

    def leave_ground(self):
        self.on_ground = self.on_ground - 1

    def reach_ground(self):
        if self.state in [PlayerSurface.JUMP_UP_STATE, PlayerSurface.DOUBLE_JUMP_STATE]:
            self.set_state(PlayerSurface.IDLE_STATE)
        self.on_ground = self.on_ground + 1
        self.double_jumped = False

    def jump(self):
        if self.on_ground > 0:
            if self.state not in [PlayerSurface.IMMUNE, PlayerSurface.HIT]:
                self.set_state(PlayerSurface.JUMP_UP_STATE)
            self.body.velocity = (self.body.velocity.x, -43)
        elif not self.double_jumped:
            if self.state not in [PlayerSurface.IMMUNE, PlayerSurface.HIT]:
                self.set_state(PlayerSurface.DOUBLE_JUMP_STATE)
            self.double_jumped = True
            self.body.velocity = (self.body.velocity.x, -43)

    def move_left(self):
        if self.state in [PlayerSurface.HIT]:
            return

        self.face_right = False
        self.body.velocity = (-30, self.body.velocity.y)
        self.surface.set_flip(True)
        if self.state in [PlayerSurface.IDLE_STATE]:
            self.set_state(PlayerSurface.RUN_STATE)

    def move_right(self):
        if self.state in [PlayerSurface.HIT]:
            return

        self.face_right = True
        self.body.velocity = (30, self.body.velocity.y)
        self.surface.set_flip(False)
        if self.state in [PlayerSurface.IDLE_STATE]:
            self.set_state(PlayerSurface.RUN_STATE)

    def stop_moving(self):
        if self.state in [PlayerSurface.HIT]:
            return

        self.body.velocity = (0, self.body.velocity.y)
        if self.state in [PlayerSurface.RUN_STATE]:
            self.set_state(PlayerSurface.IDLE_STATE)


class Camera:
    def __init__(self, game):
        self.game = game
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        self.offset_x = self.game.player.body.position.x - SCREEN_WIDTH/2
        self.offset_y = self.game.player.body.position.y - SCREEN_HEIGHT/2

        if self.offset_x < 0:
            self.offset_x = 0
        elif self.offset_x > MAP_WIDTH * TILE_WIDTH * SCALE - SCREEN_WIDTH:
            self.offset_x = MAP_WIDTH * TILE_WIDTH * SCALE - SCREEN_WIDTH

        if self.offset_y < 0:
            self.offset_y = 0
        elif self.offset_y > MAP_HEIGHT * TILE_HEIGHT * SCALE - SCREEN_HEIGHT:
            self.offset_y = MAP_HEIGHT * TILE_HEIGHT * SCALE - SCREEN_HEIGHT
