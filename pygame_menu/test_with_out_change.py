import pygame
import sys

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOARD_SIZE = 3
CIRCLE_RADIUS = 40
LINE_WIDTH = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class MorabarabaGame:
    def __init__(self):
        self.current_player = 'X'
        self.scores = {'X': 0, 'O': 0}

    def make_move(self, row, col):
        # TODO: Implement the logic to make a move
        pass

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def check_winner(self):
        # TODO: Implement the logic to check for a winner
        pass


class MorabaScreen:
    def __init__(self):
        self.game = MorabarabaGame()
        self.board_position = (
            (SCREEN_WIDTH - (BOARD_SIZE * 100)) // 2,
            (SCREEN_HEIGHT - (BOARD_SIZE * 100)) // 2
        )
        self.circle_positions = [
            [
                (self.board_position[0] + j * 100, self.board_position[1] + i * 100)
                for j in range(BOARD_SIZE)
            ]
            for i in range(BOARD_SIZE)
        ]

    def draw_labels(self, screen):
        font = pygame.font.Font(None, 36)
        player_text = f"Current Player: {self.game.current_player}"
        player_label = font.render(player_text, True, WHITE)
        player_rect = player_label.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
        screen.blit(player_label, player_rect)

        score_text = f"Scores - X: {self.game.scores['X']} | O: {self.game.scores['O']}"
        score_label = font.render(score_text, True, WHITE)
        score_rect = score_label.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
        screen.blit(score_label, score_rect)

    def draw_board(self, screen):
        pygame.draw.rect(screen, WHITE, (
            self.board_position[0] - 10,
            self.board_position[1] - 10,
            BOARD_SIZE * 100 + 20,
            BOARD_SIZE * 100 + 20
        ))
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                pygame.draw.circle(screen, WHITE, self.circle_positions[i][j], CIRCLE_RADIUS, LINE_WIDTH)

    def check_click(self, position):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                circle_pos = self.circle_positions[i][j]
                distance = pygame.math.Vector2(position) - pygame.math.Vector2(circle_pos)
                if distance.length() <= CIRCLE_RADIUS:
                    self.game.make_move(i, j)
                    return

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Morabaraba")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.check_click(pygame.mouse.get_pos())

            screen.fill(BLACK)
            self.draw_labels(screen)
            self.draw_board(screen)
            pygame.display.flip()


if __name__ == '__main__':
    game_screen = MorabaScreen()
    game_screen.main()