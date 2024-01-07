from frontend import fade_in, load_image, load_sound, load_font
import engine as eng
import pygame


class Screen:
    _sfc_well = None
    _sfc_score = None
    _sfc_next = None
    _snd_drop = None
    _snd_line = None
    _bg_well = None
    _bg_score = None
    _bg_next = None
    _bg_game = None
    _font_score = None
    _bricks = []

    def __init__(self, surface):
        surface.fill((0, 0, 0))
        self._bg_well = load_image(f"well.png")
        self._bg_next = load_image("next.png")
        self._bg_score = load_image("score.png")
        bricks = [f"brick{n}.png" for n in range(1, 8)]
        self._bricks = list(map(load_image, bricks))
        self._snd_drop = load_sound("drop.wav")
        self._snd_line = load_sound("line.wav")
        self._font_score = load_font("pocket_calculator.ttf", 18)

        self._sfc_well = surface.subsurface(220, 0, 220, 480)
        self._sfc_next = surface.subsurface(480, 20, 120, 120)
        self._sfc_score = surface.subsurface(60, 20, 120, 120)
        self._sfc_well.blit(self._bg_well, (0, 0))
        self._sfc_next.blit(self._bg_next, (0, 0))
        self._sfc_score.blit(self._bg_score, (0, 0))
        fade_in(surface)

    def connect(self, bus):
        bus.subscribe(eng.EV_WELL_CHANGE, self.render_well)
        bus.subscribe(eng.EV_SCORE_CHANGE, self.render_score)
        bus.subscribe(eng.EV_SHAPE_CHANGE, self.render_next)
        bus.subscribe(eng.EV_SHAPE_DROP, self._handle_lines)

    def disconnect(self, bus):
        bus.unsubscribe(eng.EV_WELL_CHANGE, self.render_well)
        bus.unsubscribe(eng.EV_SCORE_CHANGE, self.render_score)
        bus.unsubscribe(eng.EV_SHAPE_CHANGE, self.render_next)
        bus.unsubscribe(eng.EV_SHAPE_DROP, self._handle_lines)

    def _handle_lines(self, lines_map):
        nlines = len(lines_map)
        if nlines > 0:
            self._snd_line.play()
            return
        self._snd_drop.play()

    def render_score(self, data):
        self._sfc_score.blit(self._bg_score, (0, 0))
        right = 98
        for line in [(0, 30), (1, 55), (2, 80)]:
            i, top = line
            txt = self._font_score.render(str(data[i]), True, (20, 255, 0))
            rect = txt.get_rect()
            rect.topright = (right, top)
            self._sfc_score.blit(txt, rect)
        pygame.display.flip()

    def render_next(self, data):
        self._sfc_next.blit(self._bg_next, (0, 0))
        for brick in data:
            attr = brick.attr
            px = brick.pos * 20
            pos = (px.x + 20, px.y + 20)
            self._sfc_next.blit(self._bricks[attr], pos)
        pygame.display.flip()

    def render_well(self, data):
        self._sfc_well.blit(self._bg_well, (0, 0))
        for brick in data:
            attr = brick.attr
            px = brick.pos * 20
            pos = (px.x + 20, px.y)
            self._sfc_well.blit(self._bricks[attr], pos)
        pygame.display.flip()
