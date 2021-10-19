import pygame as pg


class BaseImage:
    def __init__(self):
        self.done = False

    def reset(self):
        self.done = True

    def get_frame(self, now):
        pass

    def rotate(self, rotation):
        raise NotImplementedError


class NoAnimation(BaseImage):
    def __init__(self, frame):
        super().__init__()
        self.original_frame = frame
        self.frame = frame

    def get_frame(self, now):
        return self.frame

    def rotate(self, rotation):
        self.frame = pg.transform.rotate(self.original_frame, rotation)


class Animation(BaseImage):
    def __init__(self, frames, fps=12, loops=-1):
        super().__init__()
        self.fps = fps
        self.frame = 0
        self.loops = loops
        self.loop_count = 0
        self.frames = frames
        self.time = None

    def reset(self):
        self.frame = 0
        self.loop_count = 0
        self.done = False
        self.time = None

    def rotate(self, rotation):
        raise NotImplementedError

    def get_frame(self, now):
        if not self.time:
            self.time = now
        if now - self.time > 1000.0 / self.fps:
            self.frame = (self.frame + 1) % len(self.frames)
            if self.frame == 0:
                self.loop_count += 1
                if self.loops != -1 and self.loop_count >= self.loops:
                    self.done = True
                    self.frame = (self.frame - 1) % len(self.frames)
            self.time = now
        return self.frames[self.frame]


class BaseSurface:
    DEFAULT_STATE = 0

    def __init__(self):
        self.states = [BaseSurface.DEFAULT_STATE]
        self.state = BaseSurface.DEFAULT_STATE
        self.default_state = BaseSurface.DEFAULT_STATE
        self.surface = pg.Surface((0, 0))
        self.images = None
        self.callback = None
        self.flip = False

    def rotate(self, rotation):
        for image in self.images.values():
            image.rotate(rotation)

    def set_flip(self, value):
        self.flip = value

    def set_state(self, state, callback=None):
        self.state = state
        self.callback = callback

    def update(self, now):
        if self.images[self.state].done:
            self.images[self.state].reset()
            if self.callback is not None:
                self.callback()
        image = self.images[self.state].get_frame(now)
        if self.flip:
            image = pg.transform.flip(image, True, False)
        self.surface = image

    def get_surface(self) -> pg.Surface:
        return self.surface
