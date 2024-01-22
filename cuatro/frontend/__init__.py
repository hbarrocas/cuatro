import pygame
import sys
import os
import engine
from pathlib import Path

DIR_RESOURCES = f"{os.path.dirname(os.path.abspath(__file__))}/resources"

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

""" Keys as returned by pygame.event.get() """
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_SPACE = pygame.K_SPACE
K_RETURN = pygame.K_RETURN
K_ESCAPE = pygame.K_ESCAPE
K_N = pygame.K_n
K_Q = pygame.K_q
K_P = pygame.K_p


def fade_in(surface):
    mask = pygame.Surface(surface.get_size())
    mask.fill((0, 0, 0))
    cross_fade(surface, mask, range(255, 0, -10))


def cross_fade(orig, repl, alpha_iter):
    sfc_size = orig.get_size()
    buffer = pygame.Surface(sfc_size)
    buffer.blit(orig, (0, 0))
    for opacity in alpha_iter:
        pygame.time.delay(40)
        orig.blit(buffer, (0, 0))
        repl.set_alpha(opacity)
        orig.blit(repl, (0, 0))
        pygame.display.flip()


def load_image(file):
    path = Path(DIR_RESOURCES, file)
    return pygame.image.load(path).convert()


def load_sound(file):
    path = Path(DIR_RESOURCES, file)
    return pygame.mixer.Sound(path)


def load_font(file, size):
    path = Path(DIR_RESOURCES, file)
    return pygame.font.Font(path, size)


def set_timer(event, period):
    pygame.time.set_timer(event, period)


class Core:
    _bus = None
    _key = {}
    display = None

    def __init__(self, ev_bus):
        self._bus = ev_bus
        self._bus.subscribe(engine.EV_CORE_EXIT, self.exit)
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.key.set_repeat(200, 50)
        size = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.display = pygame.display.set_mode(size)

    def _key_map(self, key):
        if key in self._key:
            self._key[key]()

    def key_map(self, keymap):
        self._key = keymap

    def exit(self, code: int):
        pygame.quit()
        sys.exit(code)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit(0)
                if event.type == pygame.KEYDOWN:
                    self._key_map(event.key)
                if event.type == engine.EV_TIMER1:
                    self._bus.publish(engine.EV_TIMER1)
