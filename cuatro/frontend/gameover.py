from frontend import load_font, load_sound, cross_fade
import pygame


class Screen:

    def __init__(self, surface):
        rect = surface.get_rect()
        buffer = pygame.Surface(surface.get_size())
        font = load_font("arcadeclassic.ttf", 60)
        slam = load_sound("slam.wav")
        game = font.render("GAME", True, (255, 128, 0))
        over = font.render("OVER", True, (255, 128, 0))
        cross_fade(surface, buffer, range(0, 130, 5))
        buffer.set_alpha(255)
        buffer.blit(surface, (0, 0))
        game_r = game.get_rect()
        over_r = over.get_rect()
        game_r.bottomright = (0, rect.centery - 5)
        over_r.topleft = (rect.right, rect.centery + 5)
        target = rect.centerx
        while rect.centerx > game_r.centerx:
            pygame.time.delay(10)
            surface.blit(buffer, (0, 0))
            shift = game_r.centerx + 15
            game_r.centerx = shift if shift < target else target
            surface.blit(game, game_r)
            pygame.display.flip()
        slam.play()
        buffer.blit(surface, (0, 0))
        pygame.time.delay(1000)
        while rect.centerx < over_r.centerx:
            pygame.time.delay(10)
            surface.blit(buffer, (0, 0))
            shift = over_r.centerx - 15
            over_r.centerx = shift if shift > target else target
            surface.blit(over, over_r)
            pygame.display.flip()
        slam.play()
        pygame.time.delay(1000)
