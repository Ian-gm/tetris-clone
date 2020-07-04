import pygame

class Button:
    def __init__(self, x, y, sx, sy):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.rect = pygame.Rect(x, y, sx, sy)
        self.pressed = False

    def mousePress(self, mouse, commit):
        if self.rect.collidepoint(mouse[0], mouse[1]):
            self.pressed = True
            if commit:
                self.pressed = False
                return True
        else:
            self.pressed = False


    def draw(self, screen, text_a, text_b, colour_a, colour_b, font, font_size):

        self.font = pygame.font.SysFont(font, font_size)

        if self.pressed:
            render_text = self.font.render(text_b, True, colour_a, None)
            render_text_rect = render_text.get_rect()
            render_text_rect.center = self.rect.center

            rect_surface = pygame.Surface((self.sx, self.sy))
            rect_surface.fill(colour_b)

            screen.blit(rect_surface, self.rect)
            screen.blit(render_text, render_text_rect)
        else:
            render_text = self.font.render(text_a, True, colour_b, None)
            render_text_rect = render_text.get_rect()
            render_text_rect.center = self.rect.center

            rect_surface = pygame.Surface((self.sx, self.sy))
            rect_surface.fill(colour_a)

            screen.blit(rect_surface, self.rect)
            screen.blit(render_text, render_text_rect)

    def drawText(self, screen, x, y, text, colour, font, font_size):

        self.font = pygame.font.SysFont(font, font_size)

        render_text = self.font.render(text, True, colour, None)
        render_text_rect = render_text.get_rect()
        render_text_rect.center = [x, y]

        screen.blit(render_text, render_text_rect)