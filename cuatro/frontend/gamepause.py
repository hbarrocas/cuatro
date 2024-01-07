from frontend import load_font, load_sound, cross_fade
import pygame

class Screen:
    _snd = None
    _buffer = None
    _surface = None

    def __init__(self, surface):
        self._snd = load_sound("pause.ogg")
        self._snd.play()
        rect = surface.get_rect()
        self._surface = surface
        self._buffer = pygame.Surface(rect.size)
        mask = pygame.Surface(rect.size)
        mask.fill((255, 255, 0))
        self._buffer.blit(surface, (0, 0))
        cross_fade(surface, mask, range(0, 80, 20))
        font = load_font("arcadeclassic.ttf", 30)
        pause = font.render("PAUSE", True, (255, 255, 0))
        pause_r = pause.get_rect()
        pause_r.center = rect.center
        surface.blit(pause, pause_r)
        pygame.display.flip()

    def restore(self):
        self._snd.play()
        cross_fade(self._surface, self._buffer, range(0, 255, 64))
        self._surface.blit(self._buffer, (0, 0))
        pygame.display.flip()
