import pygame as pg
import pygame.time

from src.state.state_machine import State
from src.common.common_objects import BackGround
from src.state.title.title_objects import Map
from src.sound.sound import music
from src.sound.sound import sound
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
        self.option_ui = None
        self.background = None
        self.title = None
        self.new_game_btn = None
        self.option_btn = None
        self.exit_btn = None
        self.option_open = False
        self.music_volume = None
        self.music_volume_increase = None
        self.music_volume_decrease = None
        self.sound_volume_increase = None
        self.sound_volume_decrease = None
        self.sfx_volume = None
        self.sfx_volume_increase = None
        self.main_ui = None
        self.sfx_volume_decrease = None
        self.back_option = None
        self.map = None
        self.reset()

    def reset(self):
        self.group_all = pg.sprite.Group()
        self.option_ui = pg.sprite.Group()
        self.main_ui = pg.sprite.Group()
        self.map = Map(self)
        self.background = BackGround()
        self.title = Text((SCREEN_WIDTH/2, SCREEN_HEIGHT * 2/8), "Herororo", "midtop")
        self.new_game_btn = Button((SCREEN_WIDTH/2, SCREEN_HEIGHT * 4/8), "New game", "midtop", self.new_game)
        self.option_btn = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5/8), "Options", "midtop", self.option_handler)
        self.exit_btn = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 6/8), "Exit", "midtop", self.exit)
        self.music_volume_decrease = Button((SCREEN_WIDTH * 7/8 - 50, SCREEN_HEIGHT * 4/8), "<", "midright", self.music_volume_decrease_handler)
        self.music_volume_increase = Button((SCREEN_WIDTH * 7/8, SCREEN_HEIGHT * 4/8), ">", "midright", self.music_volume_increase_handler)
        self.sound_volume_decrease = Button((SCREEN_WIDTH * 7 / 8 - 50, SCREEN_HEIGHT * 5 / 8), "<", "midright",
                                            self.sound_volume_decrease_handler)
        self.sound_volume_increase = Button((SCREEN_WIDTH * 7 / 8, SCREEN_HEIGHT * 5 / 8), ">", "midright",
                                            self.sound_volume_increase_handler)
        self.back_option = Button((SCREEN_WIDTH/2, SCREEN_HEIGHT * 6 / 8), "Back", "midtop", self.back_from_ui)
        self.music_volume = Text((SCREEN_WIDTH * 1/8, SCREEN_HEIGHT * 4/8), "Music volume " + str(int(music.get_music_volume())), "midleft")
        self.sfx_volume = Text((SCREEN_WIDTH * 1/8, SCREEN_HEIGHT * 5/8), "Sound volume " + str(int(sound.get_sound_volume())), "midleft")
        for group in self.map.layers:
            self.group_all.add(*group.sprites())
        self.main_ui.add(self.new_game_btn)
        self.main_ui.add(self.option_btn)
        self.main_ui.add(self.exit_btn)
        self.group_all.add(self.title)
        self.option_ui.add(self.music_volume)
        self.option_ui.add(self.sfx_volume)
        self.option_ui.add(self.music_volume_increase)
        self.option_ui.add(self.music_volume_decrease)
        self.option_ui.add(self.sound_volume_decrease)
        self.option_ui.add(self.sound_volume_increase)
        self.option_ui.add(self.back_option)
        self.option_open = False

    def music_volume_decrease_handler(self):
        music.set_music_volume(max(0, music.get_music_volume() - 10))
        self.music_volume.set_text("Music volume " + str(int(music.get_music_volume())))

    def music_volume_increase_handler(self):
        music.set_music_volume(min(100, music.get_music_volume() + 10))
        self.music_volume.set_text("Music volume " + str(int(music.get_music_volume())))

    def sound_volume_decrease_handler(self):
        sound.set_sound_volume(max(0, sound.get_sound_volume() - 10))
        self.sfx_volume.set_text("Sound volume " + str(int(sound.get_sound_volume())))

    def sound_volume_increase_handler(self):
        sound.set_sound_volume(min(100, sound.get_sound_volume() + 10))
        self.sfx_volume.set_text("Sound volume " + str(int(sound.get_sound_volume())))

    def back_from_ui(self):
        self.option_open = False

    def exit(self):
        pygame.time.set_timer(pygame.QUIT, 100, 1)

    def option_handler(self):
        self.option_open = True

    def new_game(self):
        self.done = True

    def startup(self, now, to_persist):
        super().startup(now, to_persist)
        music.load("title.mp3")
        music.start()
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
                if not self.option_open:
                    self.new_game_btn.click(event.pos)
                    self.exit_btn.click(event.pos)
                    self.option_btn.click(event.pos)
                else:
                    self.music_volume_decrease.click(event.pos)
                    self.music_volume_increase.click(event.pos)
                    self.sound_volume_decrease.click(event.pos)
                    self.sound_volume_increase.click(event.pos)
                    self.back_option.click(event.pos)

    def update(self, now, mouse_pos, keyboard):
        self.group_all.update(now)
        self.background.update(now)
        if not self.option_open:
            self.main_ui.update(now)
        else:
            self.option_ui.update(now)

    def draw(self, surface, interpolate):
        surface.blit(self.background.image, self.background.rect)
        self.group_all.draw(surface)
        if not self.option_open:
            self.main_ui.draw(surface)
        else:
            self.option_ui.draw(surface)
