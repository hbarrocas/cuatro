from frontend import load_font, cross_fade
import pygame


class Screen:

    def __init__(self, surface):
        rect = surface.get_rect()
        bg = pygame.Surface(rect.size)
        bg.fill((0, 0, 0))
        cross_fade(surface, bg, range(0, 255, 10))
        font_title = load_font("arcadeclassic.ttf", 50)
        font_option = load_font("arcadeclassic.ttf", 20)
        title = font_title.render("CUATRO", True, (255, 255, 0))
        title_r = title.get_rect()
        title_r.midtop = (rect.centerx, 20)
        surface.blit(title, title_r)
        opt_left = title_r.left + 20
        options = [
            ("N - New game", (opt_left, 100)),
            ("Q - Quit", (opt_left, 140))
        ]
        colour = (255, 100, 0)
        for opt in options:
            string, position = opt
            txt = font_option.render(string, True, colour)
            surface.blit(txt, position)
        pygame.display.flip()
