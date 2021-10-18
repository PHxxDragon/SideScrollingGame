import pygame as pg
import pygame.time

from src.state.state_machine import State
from src.common.common_objects import BackGround
from src.state.title.title_objects import Map
from src.common.common_objects import Button
from src.common.common_objects import Text
from src.common.config import SCREEN_WIDTH
from src.common.config import SCREEN_HEIGHT


class TitleScreen(State):
    def __init__(self):
        super().__init__()
        self.name = "TITLE"
        self.next_state_name = "GAME"
        self.group_all = None
        self.background = None
        self.title = None
        self.new_game_btn = None
        self.option_btn = None
        self.exit_btn = None
        self.map = None
        self.reset()

    def reset(self):
        self.group_all = pg.sprite.Group()
        self.map = Map(self)
        self.background = BackGround()
        self.title = Text((SCREEN_WIDTH/2, SCREEN_HEIGHT * 2/8), "Herororo", "midtop")
        self.new_game_btn = Button((SCREEN_WIDTH/2, SCREEN_HEIGHT * 4/8), "New game", "midtop", self.new_game)
        self.option_btn = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5/8), "Options", "midtop", self.option_handler)
        self.exit_btn = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 6/8), "Exit", "midtop", self.exit)
        for group in self.map.layers:
            self.group_all.add(*group.sprites())
        self.group_all.add(self.new_game_btn)
        self.group_all.add(self.option_btn)
        self.group_all.add(self.exit_btn)
        self.group_all.add(self.title)

    def exit(self):
        pygame.time.set_timer(pygame.QUIT, 100, 1)

    def option_handler(self):
        pass

    def new_game(self):
        self.done = True

    def startup(self, now, to_persist):
        super().startup(now, to_persist)
        self.reset()

    def cleanup(self):
        self.group_all = None
        self.background = None
        self.title = None
        self.new_game_btn = None
        self.option_btn = None
        self.exit_btn = None
        self.map = None
        return super().cleanup()

    def accept_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.new_game_btn.click(event.pos)
                self.exit_btn.click(event.pos)
                self.option_btn.click(event.pos)

    def update(self, now, mouse_pos, keyboard):
        self.group_all.update(now)
        self.background.update(now)

    def draw(self, surface, interpolate):
        surface.blit(self.background.image, self.background.rect)
        self.group_all.draw(surface)
