from pygame import mixer
import os

PROJECT_DIR = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
RESOURCE_DIR = os.path.join(PROJECT_DIR, "resources")
sounds = {}


class Music:
    def __init__(self):
        mixer.init()

    @staticmethod
    def load(song_name):
        song_path = os.path.join(RESOURCE_DIR, "music", song_name)
        mixer.music.load(song_path)

    @staticmethod
    def start():
        mixer.music.play(loops=-1)


class Sound:
    def __init__(self):
        mixer.init()

    @staticmethod
    def load_sound(sound_name):
        if sound_name in sounds:
            sound_path = os.path.join(RESOURCE_DIR, "music", "hit.ogg")
            sounds[sound_name] = mixer.Sound(sound_path)
        return sounds[sound_name]

    def play_sound(self, sound_name):
        sound = self.load_sound(sound_name)
        sound.play()
