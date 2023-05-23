import pygame
from pygame.locals import *

class MainMenuItem:
    def __init__(self, text, position, callback):
        self.text = text
        self.position = position
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(self.position[0], self.position[1], 200, 50)
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()
class MainMenu:
    def __init__(self):
        pygame.init()

        self.screen_size = (680, 680)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Main Menu")

        self.start_item = MainMenuItem("Start", (245, 300), self.start_game)

        self.text_font = pygame.font.Font(None, 50)
        self.additional_text = "Welcome to Morabaraba!"
    
    def start_game(self):
        game_screen = MorabaScreen()
        game_screen.main()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.start_item.handle_event(event)

            self.screen.fill((0, 0, 0))
            self.start_item.draw(self.screen)

            text_surface = self.text_font.render(self.additional_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, 190))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

        pygame.quit()
class MorabaScreen:
    def __init__(self):
        pygame.init()

        self.screen_size = (680, 680)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Morabaraba")

        self.rows = 7
        self.cols = 7
        self.gap = self.screen_size[0] // (self.cols + 1)
        self.slot_size = self.gap // 2

        self.clock = pygame.time.Clock()

    def draw_board(self):
        self.screen.fill((0, 0, 0))

        for row in range(self.rows):
            for col in range(self.cols):
                pygame.draw.rect(self.screen, (255, 255, 255), (row * self.gap, col * self.gap, self.slot_size, self.slot_size))
                pygame.draw.circle(self.screen, (0, 0, 255), (row * self.gap + self.slot_size // 2, col * self.gap + self.slot_size // 2), self.slot_size // 2 - 2, 0)

        pygame.display.flip()

    def main(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_board()
            self.clock.tick(60)

        pygame.quit()
menu = MainMenu()
menu.run()
