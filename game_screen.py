import pygame

class MorabaScreen():
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Define board attributes
        self.board_size = (680, 680)  # size of the board
        self.slot_size = 60  # size of each slot
        self.rows = 7  # number of rows
        self.cols = 7  # number of columns
        self.gap = 34  # gap between each slot


        # Define colors
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.dots_line = '#1D700F'

        # Initialize the players' colors
        self.player1_color = self.BLUE
        self.player2_color = self.RED

        # Initialize the current player
        self.current_player = 1

        # Initialize the selected circles for each player
        self.player1_selected = set()
        self.player2_selected = set()

        # Initialize the screen
        self.screen = pygame.display.set_mode(self.board_size)
        pygame.display.set_caption("Morabaraba Board")

        # Set up a clock for the game loop
        self.clock = pygame.time.Clock()

        self.board_list = [(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5), (2, 2),
                    (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),(3,3), (3, 4), (3, 5),
                    (3, 6), (4, 2), (4, 3), (4, 4), (5, 1), (5, 3), (5, 5),
                    (6, 0), (6, 3), (6, 6)]

        # Declare the circle_data dictionary
        self.circle_data = {}
        for (r, c) in self.board_list:
            x = c * self.slot_size + self.gap * (c + 1)
            y = r * self.slot_size + self.gap * (r + 1)
            self.circle_data[(r, c)] = {
                'position': (x + 30, y + 30),
                'color': self.dots_line
            }


        self.main()

    # Draw the board
    def draw_board(self):
        self.screen.fill(self.WHITE)  # fill the screen with white
        pygame.draw.rect(self.screen, "black", (0, 0, 680, 680))

        # ... Existing code ...
        # rect1
        pygame.draw.line(self.screen, self.dots_line, (64, 64), (680 - 64, 64), 4)
        pygame.draw.line(self.screen, self.dots_line, (64, 64), (64, 680 - 64), 4)
        pygame.draw.line(self.screen, self.dots_line, (680 - 55, 64), (680 - 55, 680 - 64), 4)
        pygame.draw.line(self.screen, self.dots_line, (64, 680 - 50), (680 - 55, 680 - 50), 4)
        # rect2
        pygame.draw.line(self.screen, self.dots_line, (155, 155), (680 - 155, 155), 4)
        pygame.draw.line(self.screen, self.dots_line, (155, 155), (155, 680 - 155), 4)
        pygame.draw.line(self.screen, self.dots_line, (680 - 145, 145), (680 - 145, 680 - 145), 4)
        pygame.draw.line(self.screen, self.dots_line, (155, 680 - 145), (680 - 145, 680 - 145), 4)
        # rect3
        pygame.draw.line(self.screen, self.dots_line, (250, 250), (680 - 250, 250), 4)
        pygame.draw.line(self.screen, self.dots_line, (250, 250), (250, 680 - 250), 4)
        pygame.draw.line(self.screen, self.dots_line, (680 - 240, 240), (680 - 240, 680 - 240), 4)
        pygame.draw.line(self.screen, self.dots_line, (250, 680 - 240), (680 - 240, 680 - 240), 4)
        # line
        pygame.draw.line(self.screen, self.dots_line, (64, 345), (345 - 80, 345), 4)
        pygame.draw.line(self.screen, self.dots_line, (345, 64), (345, 345 - 80), 4)
        pygame.draw.line(self.screen, self.dots_line, (450, 345), (680 - 64, 345), 4)
        pygame.draw.line(self.screen, self.dots_line, (345, 445), (345, 680 - 64), 4)
        # line
        pygame.draw.line(self.screen, self.dots_line, (64, 64), (250, 250), 6)
        pygame.draw.line(self.screen, self.dots_line, (64, 680 - 55), (260, 680 - 250), 6)
        pygame.draw.line(self.screen, self.dots_line, (680 - 250, 260), (680 - 55, 64), 6)
        pygame.draw.line(self.screen, self.dots_line, (445, 445), (680 - 50, 680 - 50), 6)

        # Draw the circles with their respective colors
        for position, data in self.circle_data.items():
            x, y = data['position']
            color = data['color']
            pygame.draw.circle(self.screen, color, (x, y), 15)
            # Draw the player's color circle
            self.is_shift(self.circle_data)

    # Check if a circle was clicked and change its color
    def check_click(self, pos):
        # global self.current_player
        for position, data in self.circle_data.items():
            x, y = data['position']
            color = data['color']
            if x - 15 <= pos[0] <= x + 15 and y - 15 <= pos[1] <= y + 15:
                if color == self.dots_line:
                    if self.current_player == 1:
                        if position not in self.player2_selected:
                            data['color'] = self.player1_color
                            self.player1_selected.add(position)
                            self.current_player = 2

                    else:
                        if position not in self.player1_selected:
                            data['color'] = self.player2_color
                            self.player2_selected.add(position)
                            self.current_player = 1
                else:
                    if self.current_player == 1 and position in self.player1_selected:
                        data['color'] = self.player1_color
                    elif self.current_player == 2 and position in self.player2_selected:
                        data['color'] = self.player2_color
                break

    # Remove the color of the selected circle
    def check_click_pic(self, pos):
        for position, data in self.circle_data.items():
            x, y = data['position']
            if x - 15 <= pos[0] <= x + 15 and y - 15 <= pos[1] <= y + 15:
                # Change the color of the clicked circle
                if data['color'] == self.player1_color:
                    data['color'] = self.dots_line
                    self.player1_selected.remove(position)
                elif data['color'] == self.player2_color:
                        data['color'] = self.dots_line
                        self.player2_selected.remove(position)
                else:
                        data['color'] = self.dots_line
                break

    # Draw the player's color circle
    def is_shift(self, circle_data):
        if self.current_player == 1:
            pygame.draw.circle(self.screen, self.player1_color, (345, 345), 30)
            circle_data[(3, 3)]['color'] = self.player1_color
        else:
            pygame.draw.circle(self.screen, self.player2_color, (345, 345), 30)
            circle_data[(3, 3)]['color'] = self.player2_color

    def main(self):
        
        # Main game loop
        run = True
        while run:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        self.check_click(mouse_pos)
                    else:         # Right mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        self.check_click_pic(mouse_pos)
            # Draw the board
            self.draw_board()

            # Update the screen
            pygame.display.update()
            # Set a tick rate to the loop (60 FPS)
            self.clock.tick(60)

        
        # Quit Pygame
        pygame.quit()


if __name__ == '__main__':
    a  = MorabaScreen()
    