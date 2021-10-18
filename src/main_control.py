import pygame as pg

from src.state.state_machine import StateMachine
from src.common.config import *


class MainControl:
    """
    Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed.
    """
    def __init__(self):
        pg.init()
        pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.now = 0.0
        self.mouse_pos = pg.mouse.get_pos()
        self.keyboard = pg.key.get_pressed()
        self.state_machine = StateMachine()

    def update(self):
        """
        Updates the currently active state.
        """
        self.now += DELTA_TIME
        self.state_machine.update(self.now, self.mouse_pos, self.keyboard)

    def draw(self, interpolate):
        if not self.state_machine.state.done:
            self.state_machine.draw(self.screen, interpolate)
            pg.display.flip()

    def events_process(self):
        """
        Process all events and pass them down to the state_machine.
        """
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.done = True
        self.state_machine.accept_events(events)
        self.mouse_pos = pg.mouse.get_pos()
        self.keyboard = pg.key.get_pressed()

    def main(self):
        """Main loop for entire program. Uses a constant timestep."""
        lag = 0.0
        while not self.done:
            lag += self.clock.tick(self.fps)
            self.events_process()
            while lag >= DELTA_TIME:
                self.update()
                lag -= DELTA_TIME
            self.draw(lag/DELTA_TIME)

