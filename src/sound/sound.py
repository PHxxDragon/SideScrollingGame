from pygame import mixer
import os

PROJECT_DIR = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
RESOURCE_DIR = os.path.join(PROJECT_DIR, "resources")
sounds = {}

MUSIC_VOLUME = 0.5
SOUND_VOLUME = 0.8


class Music:
    def __init__(self):
        mixer.init()

    @staticmethod
    def load(song_name):
        song_path = os.path.join(RESOURCE_DIR, "sound", song_name)
        mixer.music.load(song_path)

    @staticmethod
    def start():
        mixer.music.set_volume(MUSIC_VOLUME)
        mixer.music.play(loops=-1)


class Sound:
    def __init__(self):
        mixer.init()
        self.load_sound("boss-hit.mp3")
        self.load_sound("cut.mp3")
        self.load_sound("fruit.wav")
        self.load_sound("heal.mp3")
        self.load_sound("slime-hit.mp3")
        self.load_sound("strong-cut.wav")
        self.load_sound("menu-click.mp3")
        self.load_sound("hit.mp3.flac")
        self.load_sound("break.mp3.flac")
        self.load_sound("player-hit.mp3")

    @staticmethod
    def load_sound(sound_name):
        if sound_name not in sounds:
            sound_path = os.path.join(RESOURCE_DIR, "sound", sound_name)
            sounds[sound_name] = mixer.Sound(sound_path)
        return sounds[sound_name]

    def play_sound(self, sound_name):
        sound = self.load_sound(sound_name)
        sound.set_volume(SOUND_VOLUME)
        sound.play()


music = Music()
sound = Sound()
