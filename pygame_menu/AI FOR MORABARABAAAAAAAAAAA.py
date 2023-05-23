import sys
import pygame
from pygame.locals import *
import subprocess
import socket
import threading

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
        # Initialize Pygame
        pygame.init()

        # Define screen attributes
        self.screen_size = (680, 680)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Main Menu")

        # Create main menu items
        self.start_item = MainMenuItem("Start", (245, 300), self.start_game)

        # Define font for the additional text
        self.text_font = pygame.font.Font(None, 50)

        # Define additional text
        self.additional_text = "Welcome to Morabaraba!"
    
    def start_game(self):
        # Create an instance of MorabaScreen and run the game
        moraba_screen = MorabaScreen(self.screen)
        moraba_screen.main()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle events for main menu items
                self.start_item.handle_event(event)

            # Draw main menu items
            self.screen.fill((0, 0, 0))
            self.start_item.draw(self.screen)

            # Draw main menu items and additional text
            self.screen.fill((0, 0, 0))
            self.start_item.draw(self.screen)

            # Render and display the additional text
            text_surface = self.text_font.render(self.additional_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2 , 190))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

        pygame.quit()

# import sys
# import pygame
# from pygame.locals import *
# import subprocess
# import socket
# import threading

class MorabaScreen:
    def __init__(self, screen):
        self.screen = screen

        # Initialize Pygame
        pygame.init()

        # Define board attributes
        self.board_size = (1000, 1000)  # size of the board
        self.slot_size = 60  # size of each slot
        self.rows = 7  # number of rows
        self.cols = 7  # number of columns
        self.gap = 34  # gap between each slot

        # Define colors
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Define AI agent variables
        self.AI_COLOR = self.BLUE
        self.MAX_DEPTH = 5

        # Create the Morabaraba board
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

        # Initialize player turn
        self.current_player = self.RED
        
        # Initialize socket variables
        self.host = 'localhost'
        self.port = 9999
        self.server_socket = None
        self.client_socket = None

    def initialize_socket(self):
        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        # Print server address
        print(f"Server listening on {self.host}:{self.port}")

        # Wait for client to connect
        self.client_socket, address = self.server_socket.accept()

        # Print client address
        print(f"Client connected from {address[0]}:{address[1]}")

    def send_message(self, message):
        self.client_socket.send(message.encode())

    def receive_message(self):
        message = self.client_socket.recv(1024).decode()
        return message

    def switch_turn(self):
        if self.current_player == self.RED:
            self.current_player = self.BLUE
        else:
            self.current_player = self.RED

    def get_legal_moves(self):
        legal_moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == ' ':
                    legal_moves.append((row, col))
        return legal_moves

    def is_winner(self, player):
        # Check rows and columns
        for i in range(self.rows):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player or \
                    self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player or \
                self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True

        return False

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_winner(self.RED) or self.is_winner(self.BLUE):
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            legal_moves = self.get_legal_moves()
            for move in legal_moves:
                row, col = move
                self.board[row][col] = self.BLUE
                eval = self.minimax(depth - 1, False)
                self.board[row][col] = ' '
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            legal_moves = self.get_legal_moves()
            for move in legal_moves:
                row, col = move
                self.board[row][col] = self.RED
                eval = self.minimax(depth - 1, True)
                self.board[row][col] = ' '
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self):
        if self.is_winner(self.BLUE):
            return 1000
        elif self.is_winner(self.RED):
            return -1000
        else:
            return 0

    def ai_move(self):
        legal_moves = self.get_legal_moves()
        best_move = None
        max_eval = float('-inf')
        for move in legal_moves:
            row, col = move
            self.board[row][col] = self.BLUE
            eval = self.minimax(self.MAX_DEPTH, False)
            self.board[row][col] = ' '
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def draw_board(self):
        self.screen.fill(self.WHITE)
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * (self.slot_size + self.gap) + self.gap
                y = row * (self.slot_size + self.gap) + self.gap
                pygame.draw.rect(self.screen, self.BLACK, (x, y, self.slot_size, self.slot_size))
                pygame.draw.circle(self.screen, self.RED, (x + self.slot_size // 2, y + self.slot_size // 2), 20)
                pygame.draw.circle(self.screen, self.BLUE, (x + self.slot_size // 2, y + self.slot_size // 2), 20)
        pygame.display.flip()

    def run_game(self):
        self.initialize_socket()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.current_player == self.RED:
                        # Player's turn
                        x, y = event.pos
                        col = x // (self.slot_size + self.gap)
                        row = y // (self.slot_size + self.gap)
                        if self.board[row][col] == ' ':
                            self.board[row][col] = self.RED
                            self.send_message(f"MOVE {row} {col}")
                            if self.is_winner(self.RED):
                                print("Player wins!")
                            else:
                                self.switch_turn()
                                self.send_message("YOUR_TURN")
                                self.draw_board()
                                # AI's turn
                                ai_row, ai_col = self.ai_move()
                                self.board[ai_row][ai_col] = self.BLUE
                                self.switch_turn()
                                if self.is_winner(self.BLUE):
                                    print("AI wins!")
                                else:
                                    self.draw_board()
                    else:
                        print("Not your turn!")
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            message = self.receive_message()
            if message.startswith("MOVE"):
                _, row, col = message.split()
                row = int(row)
                col = int(col)
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.BLUE
                    if self.is_winner(self.BLUE):
                        print("AI wins!")
                    else:
                        self.switch_turn()
                        self.draw_board()
                else:
                    print("Invalid move!")
            elif message == "YOUR_TURN":
                self.switch_turn()
                self.draw_board()

            pygame.time.wait(100)


# Create the game window
screen = pygame.display.set_mode((1000, 1000))

# Create an instance of the MorabaScreen class
game = MorabaScreen(screen)

# Run the game
game.run_game()

import sys
import pygame
from pygame.locals import *
import subprocess
import socket
import threading

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
        # Initialize Pygame
        pygame.init()

        # Define screen attributes
        self.screen_size = (680, 680)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Main Menu")

        # Create main menu items
        self.start_item = MainMenuItem("Start", (245, 300), self.start_game)

        # Define font for the additional text
        self.text_font = pygame.font.Font(None, 50)

        # Define additional text
        self.additional_text = "Welcome to Morabaraba!"
    
    def start_game(self):
        # Create an instance of MorabaScreen and run the game
        moraba_screen = MorabaScreen(self.screen)
        moraba_screen.run_game()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle events for main menu items
                self.start_item.handle_event(event)

            # Draw main menu items and additional text
            self.screen.fill((0, 0, 0))
            self.start_item.draw(self.screen)

            # Render and display the additional text
            text_surface = self.text_font.render(self.additional_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2 , 190))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

        pygame.quit()

class MorabaScreen:
    def __init__(self, screen):
        self.screen = screen

        # Initialize Pygame
        pygame.init()

        # Define board attributes
        self.board_size = (1000, 1000)  # size of the board
        self.slot_size = 60  # size of each slot
        self.rows = 7  # number of rows
        self.cols = 7  # number of columns
        self.gap = 34  # gap between each slot

        # Define colors
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Define AI agent variables
        self.AI_COLOR = self.BLUE
        self.MAX_DEPTH = 5

        # Create the Morabaraba board
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

        # Initialize player turn
        self.current_player = self.RED
        
        # Initialize socket variables
        self.host = 'localhost'
        self.port = 9999
        self.server_socket = None
        self.client_socket = None

    # Rest of the code remains the same...

# Create the game window
screen = pygame.display.set_mode((1000, 1000))

# Create an instance of the MainMenu class
menu = MainMenu()

# Run the main menu
menu.run()

