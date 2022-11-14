import pygame.font


class Hs:

    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 700, 80
        self.hs_color = (241, 109, 63)
        self.text_color = (255, 235, 205)
        self.font = pygame.font.SysFont(None, 96, bold=True)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = self.screen_rect.midtop

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.hs_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_hs(self):
        self.screen.fill(self.hs_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
